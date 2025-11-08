import pandas as pd

# 读取男生食谱数据
male_diet = pd.read_excel('男食谱1.xlsx')

# 根据数据框的实际列数调整列名
male_diet.columns = ['食物名称', '主要成分', '食物编码', '可食部（克/份）', '食用份数', '用餐时间']

# 确保'可食部（克/份）'和'食用份数'为数值类型
male_diet['可食部（克/份）'] = pd.to_numeric(male_diet['可食部（克/份）'], errors='coerce')
male_diet['食用份数'] = pd.to_numeric(male_diet['食用份数'], errors='coerce')

# 导入所有食物成分数据
food_nutrient_data = pd.read_excel('所有食物成分数据.xlsx')
food_nutrient_data.columns = ['主要成分', '蛋白质 (g/100g)', '脂肪 (g/100g)', '碳水化合物 (g/100g)',
                              '膳食纤维 (g/100g)', '酒精 (g/100g)', '钙 (mg/100g)', '铁 (mg/100g)',
                              '锌 (mg/100g)', '维生素A (µg/100g)', '维生素B1 (mg/100g)', '维生素B2 (mg/100g)',
                              '维生素C (mg/100g)', '异亮氨酸 (mg/g蛋白质)', '亮氨酸 (mg/g蛋白质)',
                              '赖氨酸 (mg/g蛋白质)', '含硫氨基酸 (mg/g蛋白质)', '芳香族氨基酸 (mg/g蛋白质)',
                              '苏氨酸 (mg/g蛋白质)', '色氨酸 (mg/g蛋白质)', '缬氨酸 (mg/g蛋白质)']

# 确保所有营养素列都是数值类型
for column in food_nutrient_data.columns[1:]:
    food_nutrient_data[column] = pd.to_numeric(food_nutrient_data[column], errors='coerce')

# 根据主要成分合并数据
male_diet_nutrition = pd.merge(male_diet, food_nutrient_data, on='主要成分', how='left')

# 计算每种食物的营养素实际摄入量
for nutrient in ['蛋白质 (g/100g)', '脂肪 (g/100g)', '碳水化合物 (g/100g)', '膳食纤维 (g/100g)',
                 '钙 (mg/100g)', '铁 (mg/100g)', '锌 (mg/100g)', '维生素A (µg/100g)',
                 '维生素B1 (mg/100g)', '维生素B2 (mg/100g)', '维生素C (mg/100g)']:
    male_diet_nutrition[nutrient] = male_diet_nutrition[nutrient] * male_diet_nutrition['可食部（克/份）'] * male_diet_nutrition['食用份数'] / 100

# 确保所有数值列不包含非数值数据
male_diet_nutrition.fillna(0, inplace=True)

# 选择需要汇总的列
columns_to_sum = ['蛋白质 (g/100g)', '脂肪 (g/100g)', '碳水化合物 (g/100g)', '膳食纤维 (g/100g)',
                 '钙 (mg/100g)', '铁 (mg/100g)', '锌 (mg/100g)', '维生素A (µg/100g)',
                 '维生素B1 (mg/100g)', '维生素B2 (mg/100g)', '维生素C (mg/100g)']

# 计算每餐的总能量及营养素摄入量，只对选定的数值列进行操作
meal_nutrition_summary = male_diet_nutrition.groupby('用餐时间')[columns_to_sum].sum()

# 计算每餐的总能量
meal_nutrition_summary['总能量 (kcal)'] = (meal_nutrition_summary['蛋白质 (g/100g)'] * 4 +
                                        meal_nutrition_summary['脂肪 (g/100g)'] * 9 +
                                        meal_nutrition_summary['碳水化合物 (g/100g)'] * 4)

# 总能量
total_energy = meal_nutrition_summary['总能量 (kcal)'].sum()

# 计算每餐能量占总能量的百分比
meal_energy_percentage = (meal_nutrition_summary['总能量 (kcal)'] / total_energy) * 100

# 输出结果
print("每餐营养摄入总结:")
print(meal_nutrition_summary)
print("每餐能量占总能量的百分比:")
print(meal_energy_percentage)
