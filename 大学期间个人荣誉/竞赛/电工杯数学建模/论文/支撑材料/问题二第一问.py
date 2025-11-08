import pandas as pd
import numpy as np
from scipy.optimize import minimize

# 数据加载
data = pd.read_excel('附件三.xlsx')

# 计算总营养成分
data['total_protein'] = data['蛋白质 (g/100g)'] * data['可食部（克/份）'] / 100
data['total_fat'] = data['脂肪 (g/100g)'] * data['可食部（克/份）'] / 100
data['total_carbs'] = data['碳水化合物 (g/100g)'] * data['可食部（克/份）'] / 100

# 计算能量
data['total_energy'] = data['total_protein'] * 4 + data['total_fat'] * 9 + data['total_carbs'] * 4

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

# 初始化缺失氨基酸列
for aa in reference_profile.keys():
    data[f'total_{aa}'] = 0


# 计算每种食物的AAS得分
def calculate_aas(row):
    min_ratio = float('inf')
    for amino_acid, ref_amount in reference_profile.items():
        col_name = f'{amino_acid} (mg/g蛋白质)'
        if col_name in row and row[col_name] > 0:
            amino_acid_content_per_100g = row[col_name] * row['蛋白质 (g/100g)'] / 100
            ratio = amino_acid_content_per_100g / ref_amount
            min_ratio = min(min_ratio, ratio)
    return min_ratio * 100 if min_ratio < float('inf') else 0


data['AAS_score'] = data.apply(calculate_aas, axis=1)


# 定义目标函数
def objective_function(x):
    return -np.sum(data['AAS_score'] * x)


# 约束条件
def constraints(x):
    constraints_list = []
    total_energy = np.sum(data['total_energy'] * x)
    constraints_list.append(total_energy - 2400 * 1.1)  # 总能量上限
    constraints_list.append(2400 * 0.9 - total_energy)  # 总能量下限

    nutrient_requirements = {
        '钙 (mg/100g)': 800,  # mg
        '铁 (mg/100g)': 12,  # mg
        '锌 (mg/100g)': 12.5,  # mg
        '维生素A (µg/100g)': 800,  # µg
        '维生素B1 (mg/100g)': 1.4,  # mg
        '维生素B2 (mg/100g)': 1.4,  # mg
        '维生素C (mg/100g)': 100  # mg
    }

    for nutrient, requirement in nutrient_requirements.items():
        total_nutrient = np.sum(data[nutrient] * x * data['可食部（克/份）'] / 100)
        constraints_list.append(total_nutrient - requirement * 1.1)  # 微量营养素上限
        constraints_list.append(requirement * 0.9 - total_nutrient)  # 微量营养素下限

    return constraints_list


# 定义约束
constr = {'type': 'ineq', 'fun': constraints}

# 设置变量的上下界，考虑半份和整数份
bounds = []
for i, row in data.iterrows():
    if row['是否可半份'] == '是':
        bounds.append((0, None))  # 允许半份的变量
    else:
        bounds.append((1, None))  # 不允许半份的变量

# 初始化变量
x0 = np.zeros(len(data))

# 解决问题
result = minimize(objective_function, x0, method='SLSQP', bounds=bounds, constraints=constr)

# 输出结果
if result.success:
    print('Solution found:')
    print('Total AAS Score:', -result.fun)  # 取负值以显示最大化的结果
    selected_items = np.where(result.x > 0)[0]
    print('Selected Food Items and Their Quantities:')
    for i in selected_items:
        print(f"{data.loc[i, '食物名称']}: {result.x[i]} portions")
else:
    print('No solution or problem with the solution.')
