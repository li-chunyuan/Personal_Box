import pandas as pd
import pulp

# 读取数据
file_path = '附件三.xlsx'  # 请确保文件路径正确
data = pd.read_excel(file_path)

# 按每份食物的可食部分，计算每种成分的总含量
data["蛋白质总量 (g)"] = data["蛋白质 (g/100g)"] * data["可食部（克/份）"] / 100
data["脂肪总量 (g)"] = data["脂肪 (g/100g)"] * data["可食部（克/份）"] / 100
data["碳水化合物总量 (g)"] = data["碳水化合物 (g/100g)"] * data["可食部（克/份）"] / 100
data["钙总量 (mg)"] = data["钙 (mg/100g)"] * data["可食部（克/份）"] / 100
data["铁总量 (mg)"] = data["铁 (mg/100g)"] * data["可食部（克/份）"] / 100
data["锌总量 (mg)"] = data["锌 (mg/100g)"] * data["可食部（克/份）"] / 100
data["维生素A总量 (µg)"] = data["维生素A (µg/100g)"] * data["可食部（克/份）"] / 100
data["维生素B1总量 (mg)"] = data["维生素B1 (mg/100g)"] * data["可食部（克/份）"] / 100
data["维生素B2总量 (mg)"] = data["维生素B2 (mg/100g)"] * data["可食部（克/份）"] / 100
data["维生素C总量 (mg)"] = data["维生素C (mg/100g)"] * data["可食部（克/份）"] / 100

# 汇总相同序号的数据
data_aggregated = data.groupby("序号").agg({
    "食物名称": 'first',
    "可食部（克/份）": 'sum',
    "价格（元/份）": 'mean',
    "是否可半份": 'first',
    "蛋白质总量 (g)": 'sum',
    "脂肪总量 (g)": 'sum',
    "碳水化合物总量 (g)": 'sum',
    "钙总量 (mg)": 'sum',
    "铁总量 (mg)": 'sum',
    "锌总量 (mg)": 'sum',
    "维生素A总量 (µg)": 'sum',
    "维生素B1总量 (mg)": 'sum',
    "维生素B2总量 (mg)": 'sum',
    "维生素C总量 (mg)": 'sum',
    "异亮氨酸 (mg/g蛋白质)": 'mean',
    "亮氨酸 (mg/g蛋白质)": 'mean',
    "赖氨酸 (mg/g蛋白质)": 'mean',
    "含硫氨基酸 (mg/g蛋白质)": 'mean',
    "芳香族氨基酸 (mg/g蛋白质)": 'mean',
    "苏氨酸 (mg/g蛋白质)": 'mean',
    "色氨酸 (mg/g蛋白质)": 'mean',
    "缬氨酸 (mg/g蛋白质)": 'mean'
}).reset_index()

# 将总量转换回每100g含量
data_aggregated["蛋白质 (g/100g)"] = data_aggregated["蛋白质总量 (g)"] / data_aggregated["可食部（克/份）"] * 100
data_aggregated["脂肪 (g/100g)"] = data_aggregated["脂肪总量 (g)"] / data_aggregated["可食部（克/份）"] * 100
data_aggregated["碳水化合物 (g/100g)"] = data_aggregated["碳水化合物总量 (g)"] / data_aggregated["可食部（克/份）"] * 100
data_aggregated["钙 (mg/100g)"] = data_aggregated["钙总量 (mg)"] / data_aggregated["可食部（克/份）"] * 100
data_aggregated["铁 (mg/100g)"] = data_aggregated["铁总量 (mg)"] / data_aggregated["可食部（克/份）"] * 100
data_aggregated["锌 (mg/100g)"] = data_aggregated["锌总量 (mg)"] / data_aggregated["可食部（克/份）"] * 100
data_aggregated["维生素A (µg/100g)"] = data_aggregated["维生素A总量 (µg)"] / data_aggregated["可食部（克/份）"] * 100
data_aggregated["维生素B1 (mg/100g)"] = data_aggregated["维生素B1总量 (mg)"] / data_aggregated["可食部（克/份）"] * 100
data_aggregated["维生素B2 (mg/100g)"] = data_aggregated["维生素B2总量 (mg)"] / data_aggregated["可食部（克/份）"] * 100
data_aggregated["维生素C (mg/100g)"] = data_aggregated["维生素C总量 (mg)"] / data_aggregated["可食部（克/份）"] * 100

# 计算每种食物的总能量
data_aggregated["总能量 (kcal)"] = (data_aggregated["蛋白质 (g/100g)"] * 4 +
                        data_aggregated["脂肪 (g/100g)"] * 9 +
                        data_aggregated["碳水化合物 (g/100g)"] * 4) * (data_aggregated["可食部（克/份）"] / 100)


# 定义早餐、午餐和晚餐的食物
breakfast_foods = data_aggregated[data_aggregated["序号"] <= 35]
lunch_foods = data_aggregated[(data_aggregated["序号"] > 35) & (data_aggregated["序号"] <= 94)]
dinner_foods = data_aggregated[data_aggregated["序号"] > 94]

# 定义所有食物种类
foods = data_aggregated["食物名称"].unique()

# 创建LP问题
prob = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# 定义决策变量
x = {}
for food in foods:
    if data_aggregated.loc[data_aggregated["食物名称"] == food, "是否可半份"].values[0] == '是':
        x[food] = pulp.LpVariable(f"x_{food}", lowBound=0, cat='Continuous')
    else:
        x[food] = pulp.LpVariable(f"x_{food}", lowBound=0, cat='Integer')

# 每种食物最多只能购买5次的约束
for food in foods:
    prob += x[food] <= 5, f"Max_Purchase_{food}"

# 目标函数：最小化总费用
prob += pulp.lpSum([x[food] * data_aggregated.loc[data_aggregated["食物名称"] == food, "价格（元/份）"].values[0] for food in foods]), "Total_Cost"

# 约束条件
# 总能量约束在±10%之内
prob += pulp.lpSum([x[food] * data_aggregated.loc[data_aggregated["食物名称"] == food, "总能量 (kcal)"].values[0] for food in foods]) >= 0.9 * 2400, "Min_Total_Energy"
prob += pulp.lpSum([x[food] * data_aggregated.loc[data_aggregated["食物名称"] == food, "总能量 (kcal)"].values[0] for food in foods]) <= 1.1 * 2400, "Max_Total_Energy"

# 蛋白质、脂肪、碳水化合物比例约束
prob += pulp.lpSum([x[food] * data_aggregated.loc[data_aggregated["食物名称"] == food, "蛋白质 (g/100g)"].values[0] * data_aggregated.loc[data_aggregated["食物名称"] == food, "可食部（克/份）"].values[0] / 100 for food in foods]) <= 0.15 * 2400 / 4, "Max_Protein"
prob += pulp.lpSum([x[food] * data_aggregated.loc[data_aggregated["食物名称"] == food, "脂肪 (g/100g)"].values[0] * data_aggregated.loc[data_aggregated["食物名称"] == food, "可食部（克/份）"].values[0] / 100 for food in foods]) >= 0.20 * 2400 / 9, "Min_Fat"
prob += pulp.lpSum([x[food] * data_aggregated.loc[data_aggregated["食物名称"] == food, "脂肪 (g/100g)"].values[0] * data_aggregated.loc[data_aggregated["食物名称"] == food, "可食部（克/份）"].values[0] / 100 for food in foods]) <= 0.30 * 2400 / 9, "Max_Fat"
prob += pulp.lpSum([x[food] * data_aggregated.loc[data_aggregated["食物名称"] == food, "碳水化合物 (g/100g)"].values[0] * data_aggregated.loc[data_aggregated["食物名称"] == food, "可食部（克/份）"].values[0] / 100 for food in foods]) >= 0.50 * 2400 / 4, "Min_Carb"
prob += pulp.lpSum([x[food] * data_aggregated.loc[data_aggregated["食物名称"] == food, "碳水化合物 (g/100g)"].values[0] * data_aggregated.loc[data_aggregated["食物名称"] == food, "可食部（克/份）"].values[0] / 100 for food in foods]) <= 0.65 * 2400 / 4, "Max_Carb"

# 微量营养素约束
prob += pulp.lpSum([x[food] * data_aggregated.loc[data_aggregated["食物名称"] == food, "钙 (mg/100g)"].values[0] * data_aggregated.loc[data_aggregated["食物名称"] == food, "可食部（克/份）"].values[0] / 100 for food in foods]) >= 800, "Min_Calcium"
prob += pulp.lpSum([x[food] * data_aggregated.loc[data_aggregated["食物名称"] == food, "铁 (mg/100g)"].values[0] * data_aggregated.loc[data_aggregated["食物名称"] == food, "可食部（克/份）"].values[0] / 100 for food in foods]) >= 12, "Min_Iron"
prob += pulp.lpSum([x[food] * data_aggregated.loc[data_aggregated["食物名称"] == food, "锌 (mg/100g)"].values[0] * data_aggregated.loc[data_aggregated["食物名称"] == food, "可食部（克/份）"].values[0] / 100 for food in foods]) >= 12.5, "Min_Zinc"
prob += pulp.lpSum([x[food] * data_aggregated.loc[data_aggregated["食物名称"] == food, "维生素A (µg/100g)"].values[0] * data_aggregated.loc[data_aggregated["食物名称"] == food, "可食部（克/份）"].values[0] / 100 for food in foods]) >= 800, "Min_VitaminA"
prob += pulp.lpSum([x[food] * data_aggregated.loc[data_aggregated["食物名称"] == food, "维生素B1 (mg/100g)"].values[0] * data_aggregated.loc[data_aggregated["食物名称"] == food, "可食部（克/份）"].values[0] / 100 for food in foods]) >= 1.4, "Min_VitaminB1"
prob += pulp.lpSum([x[food] * data_aggregated.loc[data_aggregated["食物名称"] == food, "维生素B2 (mg/100g)"].values[0] * data_aggregated.loc[data_aggregated["食物名称"] == food, "可食部（克/份）"].values[0] / 100 for food in foods]) >= 1.4, "Min_VitaminB2"
prob += pulp.lpSum([x[food] * data_aggregated.loc[data_aggregated["食物名称"] == food, "维生素C (mg/100g)"].values[0] * data_aggregated.loc[data_aggregated["食物名称"] == food, "可食部（克/份）"].values[0] / 100 for food in foods]) >= 100, "Min_VitaminC"

# 食物种类与类别要求：每天至少12种不同的食物
prob += pulp.lpSum([pulp.LpVariable(f"binary_{food}", cat='Binary') for food in foods]) >= 12, "Min_Food_Variety"

# 餐次分配
# 早餐：总能量的25%-35%
prob += pulp.lpSum([x[food] * data_aggregated.loc[data_aggregated["食物名称"] == food, "总能量 (kcal)"].values[0] for food in breakfast_foods["食物名称"].unique()]) >= 0.25 * 2400, "Min_Breakfast_Energy"
prob += pulp.lpSum([x[food] * data_aggregated.loc[data_aggregated["食物名称"] == food, "总能量 (kcal)"].values[0] for food in breakfast_foods["食物名称"].unique()]) <= 0.35 * 2400, "Max_Breakfast_Energy"

# 午餐：总能量的30%-40%
prob += pulp.lpSum([x[food] * data_aggregated.loc[data_aggregated["食物名称"] == food, "总能量 (kcal)"].values[0] for food in lunch_foods["食物名称"].unique()]) >= 0.30 * 2400, "Min_Lunch_Energy"
prob += pulp.lpSum([x[food] * data_aggregated.loc[data_aggregated["食物名称"] == food, "总能量 (kcal)"].values[0] for food in lunch_foods["食物名称"].unique()]) <= 0.40 * 2400, "Max_Lunch_Energy"

# 晚餐：总能量的30%-40%
prob += pulp.lpSum([x[food] * data_aggregated.loc[data_aggregated["食物名称"] == food, "总能量 (kcal)"].values[0] for food in dinner_foods["食物名称"].unique()]) >= 0.30 * 2400, "Min_Dinner_Energy"
prob += pulp.lpSum([x[food] * data_aggregated.loc[data_aggregated["食物名称"] == food, "总能量 (kcal)"].values[0] for food in dinner_foods["食物名称"].unique()]) <= 0.40 * 2400, "Max_Dinner_Energy"

# 求解问题
prob.solve()

# 输出结果
breakfast_result = {}
lunch_result = {}
dinner_result = {}

for food in foods:
    if x[food].varValue > 0:
        if food in breakfast_foods["食物名称"].unique():
            breakfast_result[food] = x[food].varValue
        elif food in lunch_foods["食物名称"].unique():
            lunch_result[food] = x[food].varValue
        elif food in dinner_foods["食物名称"].unique():
            dinner_result[food] = x[food].varValue

print("早餐选择的菜品及份数：")
for food, amount in breakfast_result.items():
    print(f"{food}: {amount} 份")

print("午餐选择的菜品及份数：")
for food, amount in lunch_result.items():
    print(f"{food}: {amount} 份")

print("晚餐选择的菜品及份数：")
for food, amount in dinner_result.items():
    print(f"{food}: {amount} 份")

print(f"Total Cost: {pulp.value(prob.objective)}")


# 计算每餐混合食物的氨基酸评分
def calculate_amino_acid_score(foods, quantities, data):
    amino_acid_scores = ["异亮氨酸 (mg/g蛋白质)", "亮氨酸 (mg/g蛋白质)", "赖氨酸 (mg/g蛋白质)",
                         "含硫氨基酸 (mg/g蛋白质)", "芳香族氨基酸 (mg/g蛋白质)", "苏氨酸 (mg/g蛋白质)",
                         "色氨酸 (mg/g蛋白质)", "缬氨酸 (mg/g蛋白质)"]

    total_protein = sum(
        [quantities[food] * data.loc[data["食物名称"] == food, "蛋白质总量 (g)"].values[0] for food in foods])
    scores = {}

    for score in amino_acid_scores:
        total_aa = sum([quantities[food] * data.loc[data["食物名称"] == food, score].values[0] for food in foods])
        scores[score] = total_aa / total_protein * 1000 if total_protein != 0 else 0

    limiting_aa_score = min(scores.values())
    return limiting_aa_score


# 计算早餐、午餐、晚餐的氨基酸评分
breakfast_score = calculate_amino_acid_score(breakfast_result.keys(), breakfast_result, data)
lunch_score = calculate_amino_acid_score(lunch_result.keys(), lunch_result, data)
dinner_score = calculate_amino_acid_score(dinner_result.keys(), dinner_result, data)


def evaluate_amino_acid_score(score):
    if score < 60:
        return "不合理"
    elif 60 <= score < 80:
        return "不够合理"
    elif 80 <= score < 90:
        return "比较合理"
    else:
        return "合理"


print("早餐氨基酸评分及评价：")
print(f"氨基酸评分: {breakfast_score}")
print(f"评价: {evaluate_amino_acid_score(breakfast_score)}")

print("午餐氨基酸评分及评价：")
print(f"氨基酸评分: {lunch_score}")
print(f"评价: {evaluate_amino_acid_score(lunch_score)}")

print("晚餐氨基酸评分及评价：")
print(f"氨基酸评分: {dinner_score}")
print(f"评价: {evaluate_amino_acid_score(dinner_score)}")
