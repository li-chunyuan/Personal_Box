import pandas as pd
from deap import base, creator, tools, algorithms
import random

# 数据加载
data = pd.read_excel('附件三.xlsx')  # 修改为正确的文件路径

# 计算每种食物的总营养成分
data['total_protein'] = data['蛋白质 (g/100g)'] * data['可食部（克/份）'] / 100
data['total_fat'] = data['脂肪 (g/100g)'] * data['可食部（克/份）'] / 100
data['total_carbs'] = data['碳水化合物 (g/100g)'] * data['可食部（克/份）'] / 100

# 计算每种食物的能量（卡路里）
data['energy_per_100g'] = (data['蛋白质 (g/100g)'] * 4) + (data['脂肪 (g/100g)'] * 9) + (
            data['碳水化合物 (g/100g)'] * 4)
data['total_energy'] = data['energy_per_100g'] * (data['可食部（克/份）'] / 100)

# 定义参考氨基酸模式
reference_profile = {
    '异亮氨酸': 40,
    '亮氨酸': 70,
    '赖氨酸': 55,
    '含硫氨基酸': 35,
    '芳香族氨基酸': 60,
    '苏氨酸': 40,
    '色氨酸': 10,
    '缬氨酸': 50
}

# 计算每种食物的AAS得分
def calculate_aas(row):
    min_ratio = float('inf')
    for amino_acid, ref_amount in reference_profile.items():
        amino_acid_content_per_100g = row[f'{amino_acid} (mg/g蛋白质)'] * row['蛋白质 (g/100g)'] / 100
        if ref_amount > 0:
            ratio = amino_acid_content_per_100g / ref_amount
            min_ratio = min(min_ratio, ratio)
    return min_ratio * 100

data['AAS_score'] = data.apply(calculate_aas, axis=1)

# 遗传算法设置
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# 初始化个体的属性，确保份数是0.5的倍数
def init_individual():
    individual = []
    for i in data.index:
        if data.loc[i, '是否可半份'] == '是':
            individual.append(round(random.uniform(0, 20)) / 2)  # 允许0.5的倍数
        else:
            individual.append(random.randint(0, 10))  # 只允许整数
    return creator.Individual(individual)

toolbox.register("individual", init_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

nutrient_requirements = {
    '钙': 800,  # mg
    '铁': 12,  # mg
    '锌': 12.5,  # mg
    '维生素A': 800,  # µg
    '维生素B1': 1.4,  # mg
    '维生素B2': 1.4,  # mg
    '维生素C': 100  # mg
}

nutrient_columns = {
    '钙': '钙 (mg/100g)',
    '铁': '铁 (mg/100g)',
    '锌': '锌 (mg/100g)',
    '维生素A': '维生素A (µg/100g)',
    '维生素B1': '维生素B1 (mg/100g)',
    '维生素B2': '维生素B2 (mg/100g)',
    '维生素C': '维生素C (mg/100g)'
}

breakfast_indices = data.index[data['序号'].isin(range(1, 36))]
lunch_indices = data.index[data['序号'].isin(range(36, 95))]
dinner_indices = data.index[data['序号'].isin(range(95, 143))]

def evalMeal(individual):
    total_energy = 0
    total_aas_score = 0
    total_nutrients = {key: 0 for key in reference_profile.keys()}
    total_nutrients.update({'钙': 0, '铁': 0, '锌': 0, '维生素A': 0, '维生素B1': 0, '维生素B2': 0, '维生素C': 0})

    total_breakfast_energy = 0
    total_lunch_energy = 0
    total_dinner_energy = 0

    for i in range(len(individual)):
        total_energy += individual[i] * data.iloc[i]['total_energy']
        total_aas_score += individual[i] * data.iloc[i]['AAS_score']

        for nutrient in total_nutrients.keys():
            if nutrient in reference_profile:
                total_nutrients[nutrient] += individual[i] * data.iloc[i][f'{nutrient} (mg/g蛋白质)'] * data.iloc[i][
                    '蛋白质 (g/100g)'] / 100
            else:
                total_nutrients[nutrient] += individual[i] * data.iloc[i][nutrient_columns[nutrient]] * data.iloc[i][
                    '可食部（克/份）'] / 100

        if i in breakfast_indices:
            total_breakfast_energy += individual[i] * data.iloc[i]['total_energy']
        elif i in lunch_indices:
            total_lunch_energy += individual[i] * data.iloc[i]['total_energy']
        elif i in dinner_indices:
            total_dinner_energy += individual[i] * data.iloc[i]['total_energy']

    # 添加能量约束和营养素约束的惩罚项
    penalty = 0

    if not (2160 <= total_energy <= 2640):
        penalty += 10000

    for nutrient, requirement in nutrient_requirements.items():
        if not (requirement * 0.9 <= total_nutrients[nutrient] <= requirement * 1.1):
            penalty += 10000

    # 餐次比约束
    if not (0.25 <= total_breakfast_energy / total_energy <= 0.35):
        penalty += 5000
    if not (0.30 <= total_lunch_energy / total_energy <= 0.40):
        penalty += 5000
    if not (0.30 <= total_dinner_energy / total_energy <= 0.40):
        penalty += 5000

    return total_aas_score - penalty,

toolbox.register("evaluate", evalMeal)
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutPolynomialBounded, low=0, up=20, eta=1.0, indpb=0.2)  # 增加范围到20以允许0.5的倍数
toolbox.register("select", tools.selTournament, tournsize=3)

population = toolbox.population(n=3000)  # 增加种群数量以增加多样性

ngen = 300  # 增加迭代次数
cxpb = 0.7  # 增加交叉概率
mutpb = 0.3  # 增加变异概率

result, log = algorithms.eaSimple(population, toolbox, cxpb, mutpb, ngen, verbose=True)

# 获取最佳个体
best_individual = tools.selBest(population, k=1)[0]
print("Best Individual = ", best_individual)

# 输出目标函数值
print("Total AAS Score = ", evalMeal(best_individual)[0])

# 将最佳个体的食物份数转换为0.5的倍数
print("Optimized Food Portions:")
for i in range(len(best_individual)):
    if best_individual[i] > 0:
        if data.iloc[i]['是否可半份'] == '是':
            print(data.iloc[i]['食物名称'], "=", round(best_individual[i] * 2) / 2)
        else:
            print(data.iloc[i]['食物名称'], "=", round(best_individual[i]))
