import pandas as pd

# 读取数据，确保路径正确
canteen_data = pd.read_excel('附件3：某高校学生食堂一日三餐主要食物信息统计表.xlsx', skiprows=1)
nutrition_data = pd.read_excel('所有食物成分数据.xlsx')

# 设置正确的列名
canteen_data.columns = ['序号', '食物名称', '主要成分', '食物编码', '可食部（克/份）', '价格（元/份）', '是否可半份']
nutrition_data.columns = ['主要成分', '蛋白质 (g/100g)', '脂肪 (g/100g)', '碳水化合物 (g/100g)', '膳食纤维 (g/100g)', '酒精 (g/100g)', '钙 (mg/100g)', '铁 (mg/100g)', '锌 (mg/100g)', '维生素A (µg/100g)', '维生素B1 (mg/100g)', '维生素B2 (mg/100g)', '维生素C (mg/100g)', '异亮氨酸 (mg/g蛋白质)', '亮氨酸 (mg/g蛋白质)', '赖氨酸 (mg/g蛋白质)', '含硫氨基酸 (mg/g蛋白质)', '芳香族氨基酸 (mg/g蛋白质)', '苏氨酸 (mg/g蛋白质)', '色氨酸 (mg/g蛋白质)', '缬氨酸 (mg/g蛋白质)']

# 删除不需要的列并转换数据类型
canteen_data.drop(columns=['食物编码'], inplace=True)
canteen_data['可食部（克/份）'] = pd.to_numeric(canteen_data['可食部（克/份）'], errors='coerce')

# 合并数据，关联的键为'主要成分'
combined_data = pd.merge(canteen_data, nutrition_data, on='主要成分', how='left')

# 计算每种食物的具体营养成分
for nutrient in ['蛋白质 (g/100g)', '脂肪 (g/100g)', '碳水化合物 (g/100g)', '膳食纤维 (g/100g)', '钙 (mg/100g)', '铁 (mg/100g)', '锌 (mg/100g)', '维生素A (µg/100g)', '维生素B1 (mg/100g)', '维生素B2 (mg/100g)', '维生素C (mg/100g)', '异亮氨酸 (mg/g蛋白质)', '亮氨酸 (mg/g蛋白质)', '赖氨酸 (mg/g蛋白质)', '含硫氨基酸 (mg/g蛋白质)', '芳香族氨基酸 (mg/g蛋白质)', '苏氨酸 (mg/g蛋白质)', '色氨酸 (mg/g蛋白质)', '缬氨酸 (mg/g蛋白质)']:
    combined_data[nutrient] = combined_data[nutrient] * combined_data['可食部（克/份）'] / 100

# 保存结果到Excel文件
combined_data.to_excel('附件三计算后结果.xlsx')

print("数据处理完成，并已保存到Excel文件。")
