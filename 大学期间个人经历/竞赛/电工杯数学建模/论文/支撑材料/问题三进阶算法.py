import pandas as pd
import pulp

# 读取数据
file_path = '附件三.xlsx'
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

# 计算氨基酸评分
data_aggregated["氨基酸评分"] = (data_aggregated[["异亮氨酸 (mg/g蛋白质)", "亮氨酸 (mg/g蛋白质)", "赖氨酸 (mg/g蛋白质)",
                          "含硫氨基酸 (mg/g蛋白质)", "芳香族氨基酸 (mg/g蛋白质)", "苏氨酸 (mg/g蛋白质)",
                          "色氨酸 (mg/g蛋白质)", "缬氨酸 (mg/g蛋白质)"]].min(axis=1))

# 定义早餐、午餐和晚餐的食物
breakfast_foods = data_aggregated[data_aggregated["序号"] <= 35]
lunch_foods = data_aggregated[(data_aggregated["序号"] > 35) & (data_aggregated["序号"] <= 94)]
dinner_foods = data_aggregated[data_aggregated["序号"] > 94]

# 定义所有食物种类
foods = data_aggregated["食物名称"].unique()

# 创建LP问题
prob = pulp.LpProblem("Weekly_Optimize_Amino_Acid_Score_and_Cost", pulp.LpMinimize)

# 定义每天的决策变量
x = {}
for day in range(1, 8):  # 一周7天
    for food in foods:
        if data_aggregated.loc[data_aggregated["食物名称"] == food, "是否可半份"].values[0] == '是':
            x[(day, food)] = pulp.LpVariable(f"x_{day}_{food}", lowBound=0, cat='Continuous')
        else:
            x[(day, food)] = pulp.LpVariable(f"x_{day}_{food}", lowBound=0, cat='Integer')

# 每种食物每天最多只能购买5次的约束
for day in range(1, 8):
    for food in foods:
        prob += x[(day, food)] <= 5, f"Max_Purchase_{day}_{food}"

# 目标函数：最小化总费用
total_cost = pulp.lpSum([x[(day, food)] * data_aggregated.loc[data_aggregated["食物名称"] == food, "价格（元/份）"].values[0] for day in range(1, 8) for food in foods])
prob += total_cost, "Total_Cost"

# 约束条件
for day in range(1, 8):
    # 总能量约束在±10%之内
    prob += pulp.lpSum([x[(day, food)] * data_aggregated.loc[data_aggregated["食物名称"] == food, "总能量 (kcal)"].values[0] for food in foods]) >= 0.9 * 2400, f"Min_Total_Energy_{day}"
    prob += pulp.lpSum([x[(day, food)] * data_aggregated.loc[data_aggregated["食物名称"] == food, "总能量 (kcal)"].values[0] for food in foods]) <= 1.1 * 2400, f"Max_Total_Energy_{day}"

    # 蛋白质、脂肪、碳水化合物比例约束
    prob += pulp.lpSum([x[(day, food)] * data_aggregated.loc[data_aggregated["食物名称"] == food, "蛋白质 (g/100g)"].values[0] * data_aggregated.loc[data_aggregated["食物名称"] == food, "可食部（克/份）"].values[0] / 100 for food in foods]) >= 0.10 * 2400 / 4, f"Min_Protein_{day}"
    prob += pulp.lpSum([x[(day, food)] * data_aggregated.loc[data_aggregated["食物名称"] == food, "蛋白质 (g/100g)"].values[0] * data_aggregated.loc[data_aggregated["食物名称"] == food, "可食部（克/份）"].values[0] / 100 for food in foods]) <= 0.15 * 2400 / 4, f"Max_Protein_{day}"
    prob += pulp.lpSum([x[(day, food)] * data_aggregated.loc[data_aggregated["食物名称"] == food, "脂肪 (g/100g)"].values[0] * data_aggregated.loc[data_aggregated["食物名称"] == food, "可食部（克/份）"].values[0] / 100 for food in foods]) >= 0.20 * 2400 / 9, f"Min_Fat_{day}"
    prob += pulp.lpSum([x[(day, food)] * data_aggregated.loc[data_aggregated["食物名称"] == food, "脂肪 (g/100g)"].values[0] * data_aggregated.loc[data_aggregated["食物名称"] == food, "可食部（克/份）"].values[0] / 100 for food in foods]) <= 0.30 * 2400 / 9, f"Max_Fat_{day}"
    prob += pulp.lpSum([x[(day, food)] * data_aggregated.loc[data_aggregated["食物名称"] == food, "碳水化合物 (g/100g)"].values[0] * data_aggregated.loc[data_aggregated["食物名称"] == food, "可食部（克/份）"].values[0] / 100 for food in foods]) >= 0.50 * 2400 / 4, f"Min_Carb_{day}"
    prob += pulp.lpSum([x[(day, food)] * data_aggregated.loc[data_aggregated["食物名称"] == food, "碳水化合物 (g/100g)"].values[0] * data_aggregated.loc[data_aggregated["食物名称"] == food, "可食部（克/份）"].values[0] / 100 for food in foods]) <= 0.65 * 2400 / 4, f"Max_Carb_{day}"

    # 微量营养素约束
    prob += pulp.lpSum([x[(day, food)] * data_aggregated.loc[data_aggregated["食物名称"] == food, "钙 (mg/100g)"].values[0] * data_aggregated.loc[data_aggregated["食物名称"] == food, "可食部（克/份）"].values[0] / 100 for food in foods]) >= 800, f"Min_Calcium_{day}"
    prob += pulp.lpSum([x[(day, food)] * data_aggregated.loc[data_aggregated["食物名称"] == food, "铁 (mg/100g)"].values[0] * data_aggregated.loc[data_aggregated["食物名称"] == food, "可食部（克/份）"].values[0] / 100 for food in foods]) >= 12, f"Min_Iron_{day}"
    prob += pulp.lpSum([x[(day, food)] * data_aggregated.loc[data_aggregated["食物名称"] == food, "锌 (mg/100g)"].values[0] * data_aggregated.loc[data_aggregated["食物名称"] == food, "可食部（克/份）"].values[0] / 100 for food in foods]) >= 12.5, f"Min_Zinc_{day}"
    prob += pulp.lpSum([x[(day, food)] * data_aggregated.loc[data_aggregated["食物名称"] == food, "维生素A (µg/100g)"].values[0] * data_aggregated.loc[data_aggregated["食物名称"] == food, "可食部（克/份）"].values[0] / 100 for food in foods]) >= 800, f"Min_VitaminA_{day}"
    prob += pulp.lpSum([x[(day, food)] * data_aggregated.loc[data_aggregated["食物名称"] == food, "维生素B1 (mg/100g)"].values[0] * data_aggregated.loc[data_aggregated["食物名称"] == food, "可食部（克/份）"].values[0] / 100 for food in foods]) >= 1.4, f"Min_VitaminB1_{day}"
    prob += pulp.lpSum([x[(day, food)] * data_aggregated.loc[data_aggregated["食物名称"] == food, "维生素B2 (mg/100g)"].values[0] * data_aggregated.loc[data_aggregated["食物名称"] == food, "可食部（克/份）"].values[0] / 100 for food in foods]) >= 1.4, f"Min_VitaminB2_{day}"
    prob += pulp.lpSum([x[(day, food)] * data_aggregated.loc[data_aggregated["食物名称"] == food, "维生素C (mg/100g)"].values[0] * data_aggregated.loc[data_aggregated["食物名称"] == food, "可食部（克/份）"].values[0] / 100 for food in foods]) >= 100, f"Min_VitaminC_{day}"

# 每天食物种类不同的约束
for day in range(2, 8):
    for food in foods:
        prob += pulp.lpSum([x[(day, food)]]) <= pulp.lpSum([x[(day-1, food)]]) + 1, f"Different_Food_{day}_{food}"

# 每周食物种类大于25种的约束
unique_foods = {food: pulp.LpVariable(f"unique_{food}", cat='Binary') for food in foods}
for food in foods:
    prob += pulp.lpSum([x[(day, food)] for day in range(1, 8)]) <= 5 * unique_foods[food], f"Max_Weekly_Food_{food}"
prob += pulp.lpSum([unique_foods[food] for food in foods]) >= 25, "Min_Weekly_Food_Variety"

# 求解问题
prob.solve()
# 输出结果
weekly_result = {day: {} for day in range(1, 8)}
for day in range(1, 8):
    for food in foods:
        if x[(day, food)].varValue > 0:
            weekly_result[day][food] = x[(day, food)].varValue

for day in range(1, 8):
    print(f"第{day}天的选择：")
    for food, amount in weekly_result[day].items():
        print(f"{food}: {amount} 份")
    print()

print(f"Total Cost: {pulp.value(prob.objective)}")

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


# 计算每天的氨基酸评分
for day in range(1, 8):
    score = calculate_amino_acid_score(weekly_result[day].keys(), weekly_result[day], data)
    print(f"第{day}天的氨基酸评分: {score}")


def evaluate_amino_acid_score(score):
    if score < 60:
        return "不合理"
    elif 60 <= score < 80:
        return "不够合理"
    elif 80 <= score < 90:
        return "比较合理"
    else:
        return "合理"


# 评价每天的氨基酸评分
for day in range(1, 8):
    score = calculate_amino_acid_score(weekly_result[day].keys(), weekly_result[day], data)
    evaluation = evaluate_amino_acid_score(score)
    print(f"第{day}天的氨基酸评分评价: {evaluation}")
