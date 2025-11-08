import pandas as pd

# 读取男生食谱数据
male_diet = pd.read_excel('问题一女生优化后数据.xlsx')

# 清洗数据
male_diet_clean = male_diet.drop([0]).reset_index(drop=True)
male_diet_clean.columns = ['食物名称', '主要成分', '食物编码', '可食部（克/份）', '食用份数']

# 完整的食物类别分类字典（基于食堂所有食物清单）
food_categories_full = {
    '白菜': '蔬菜、菌藻、水果类',
    '扁豆': '蔬菜、菌藻、水果类',
    '菠菜': '蔬菜、菌藻、水果类',
    '橙': '蔬菜、菌藻、水果类',
    '带鱼': '畜、禽、鱼、蛋类及制品',
    '稻米': '谷、薯类',
    '地瓜': '谷、薯类',
    '豆腐': '奶、干豆、坚果、种子类及制品',
    '豆芽': '蔬菜、菌藻、水果类',
    '豆油': '植物油类',
    '粉条': '谷、薯类',
    '干豆腐': '奶、干豆、坚果、种子类及制品',
    '海带': '蔬菜、菌藻、水果类',
    '胡萝卜': '蔬菜、菌藻、水果类',
    '花生米': '奶、干豆、坚果、种子类及制品',
    '黄豆': '奶、干豆、坚果、种子类及制品',
    '黄瓜': '蔬菜、菌藻、水果类',
    '黄花鱼': '畜、禽、鱼、蛋类及制品',
    '火腿肠': '畜、禽、鱼、蛋类及制品',
    '鸡蛋': '畜、禽、鱼、蛋类及制品',
    '鸡肉': '畜、禽、鱼、蛋类及制品',
    '韭菜': '蔬菜、菌藻、水果类',
    '卷心菜': '蔬菜、菌藻、水果类',
    '萝卜': '蔬菜、菌藻、水果类',
    '蜜瓜': '蔬菜、菌藻、水果类',
    '明太鱼': '畜、禽、鱼、蛋类及制品',
    '木耳': '蔬菜、菌藻、水果类',
    '南瓜': '蔬菜、菌藻、水果类',
    '牛奶': '奶、干豆、坚果、种子类及制品',
    '牛肉': '畜、禽、鱼、蛋类及制品',
    '苹果': '蔬菜、菌藻、水果类',
    '葡萄': '蔬菜、菌藻、水果类',
    '荞麦面': '谷、薯类',
    '茄汁沙丁鱼': '畜、禽、鱼、蛋类及制品',
    '茄子': '蔬菜、菌藻、水果类',
    '芹菜': '蔬菜、菌藻、水果类',
    '青椒': '蔬菜、菌藻、水果类',
    '酸菜': '蔬菜、菌藻、水果类',
    '酸奶': '奶、干豆、坚果、种子类及制品',
    '蒜台': '蔬菜、菌藻、水果类',
    '土豆': '谷、薯类',
    '五花猪肉': '畜、禽、鱼、蛋类及制品',
    '西瓜': '蔬菜、菌藻、水果类',
    '西红柿': '蔬菜、菌藻、水果类',
    '香菇': '蔬菜、菌藻、水果类',
    '香蕉': '蔬菜、菌藻、水果类',
    '小麦粉': '谷、薯类',
    '小米': '谷、薯类',
    '杏鲍菇': '蔬菜、菌藻、水果类',
    '洋葱': '蔬菜、菌藻、水果类',
    '油菜': '蔬菜、菌藻、水果类',
    '柚子': '蔬菜、菌藻、水果类',
    '鱼丸': '畜、禽、鱼、蛋类及制品',
    '玉米面': '谷、薯类',
    '炸鸡块': '畜、禽、鱼、蛋类及制品',
    '芝麻油': '植物油类',
    '猪排骨': '畜、禽、鱼、蛋类及制品',
    '猪肉': '畜、禽、鱼、蛋类及制品',
    '猪肉瘦': '畜、禽、鱼、蛋类及制品',
    '紫菜': '蔬菜、菌藻、水果类'
}

# 根据主要成分添加类别信息
male_diet_clean['类别'] = male_diet_clean['主要成分'].map(food_categories_full)

# 统计每类食物的数量
category_counts = male_diet_clean['类别'].value_counts()

# 判断五大类食物是否齐全
categories_present = set(category_counts.index)
required_categories = {'谷、薯类', '蔬菜、菌藻、水果类', '畜、禽、鱼、蛋类及制品', '奶、干豆、坚果、种子类及制品', '植物油类'}
all_categories_present = required_categories.issubset(categories_present)

# 计算食物种类总数
total_food_varieties = male_diet_clean['主要成分'].nunique()

# 导入所有食物成分数据
food_nutrient_data = pd.read_excel('所有食物成分数据.xlsx')

# 计算每种食物的营养素含量
male_diet_nutrition = male_diet_clean.merge(food_nutrient_data, left_on='主要成分', right_on='食物')

# 计算实际摄入量
for nutrient in ['蛋白质 (g/100g)', '脂肪 (g/100g)', '碳水化合物 (g/100g)', '膳食纤维(g/100g)',
                 '钙 (mg/100g)', '铁 (mg/100g)', '锌 (mg/100g)', '维生素A (µg/100g)',
                 '维生素B1 (mg/100g)', '维生素B2 (mg/100g)', '维生素C (mg/100g)']:
    male_diet_nutrition[nutrient] = male_diet_nutrition[nutrient] * male_diet_nutrition['可食部（克/份）'] * male_diet_nutrition['食用份数'] / 100

# 计算每日总摄入量
total_nutrition = male_diet_nutrition[['蛋白质 (g/100g)', '脂肪 (g/100g)', '碳水化合物 (g/100g)',
                                       '膳食纤维(g/100g)', '钙 (mg/100g)', '铁 (mg/100g)',
                                       '锌 (mg/100g)', '维生素A (µg/100g)', '维生素B1 (mg/100g)',
                                       '维生素B2 (mg/100g)', '维生素C (mg/100g)']].sum()

# 实际能量摄入计算
protein_energy = total_nutrition['蛋白质 (g/100g)'] * 4
fat_energy = total_nutrition['脂肪 (g/100g)'] * 9
carb_energy = total_nutrition['碳水化合物 (g/100g)'] * 4

total_energy = protein_energy + fat_energy + carb_energy

# 各宏量营养素的能量占比
protein_percentage = (protein_energy / total_energy) * 100
fat_percentage = (fat_energy / total_energy) * 100
carb_percentage = (carb_energy / total_energy) * 100
# 各宏量营养素的能量占比
protein_percentage = (protein_energy / total_energy) * 100
fat_percentage = (fat_energy / total_energy) * 100
carb_percentage = (carb_energy / total_energy) * 100

# 参考蛋白质氨基酸评分模式（mg/g蛋白质）
reference_amino_acid_scores = {
    '异亮氨酸': 40,
    '亮氨酸': 70,
    '赖氨酸': 55,
    '含硫氨基酸': 35,
    '芳香族氨基酸': 60,
    '苏氨酸': 40,
    '色氨酸': 10,
    '缬氨酸': 50
}

# 计算每种食物的必需氨基酸评分（AAS）
amino_acid_scores = {}
for amino_acid in reference_amino_acid_scores.keys():
    food_amino_acid = male_diet_nutrition[amino_acid + ' (mg/g蛋白质)'] * male_diet_nutrition['蛋白质 (g/100g)']
    total_food_amino_acid = food_amino_acid.sum() / male_diet_nutrition['蛋白质 (g/100g)'].sum()
    AAS = (total_food_amino_acid / reference_amino_acid_scores[amino_acid]) * 100
    amino_acid_scores[amino_acid] = AAS

# 查找第一限制氨基酸
first_limiting_amino_acid = min(amino_acid_scores, key=amino_acid_scores.get)
first_limiting_AAS = amino_acid_scores[first_limiting_amino_acid]

# 结果输出
print(f"蛋白质能量占比: {protein_percentage}%")
print(f"脂肪能量占比: {fat_percentage}%")
print(f"碳水化合物能量占比: {carb_percentage}%")
print("必需氨基酸评分（AAS）:")
for amino_acid, score in amino_acid_scores.items():
    print(f"{amino_acid}: {score}")
print(f"第一限制氨基酸: {first_limiting_amino_acid}")
print(f"第一限制氨基酸评分: {first_limiting_AAS}")



# 输出结果
# 输出结果
print(f"类别统计:\n{category_counts}")
print(f"是否包含所有五大类食物: {all_categories_present}")
print(f"食物种类总数: {total_food_varieties}")
print(f"每日总摄入量:\n{total_nutrition}")
print(f"蛋白质能量: {protein_energy} kcal")
print(f"脂肪能量: {fat_energy} kcal")
print(f"碳水化合物能量: {carb_energy} kcal")
print(f"总能量: {total_energy} kcal")
print(f"蛋白质能量占比: {protein_percentage:.2f}%")
print(f"脂肪能量占比: {fat_percentage:.2f}%")
print(f"碳水化合物能量占比: {carb_percentage:.2f}%")


