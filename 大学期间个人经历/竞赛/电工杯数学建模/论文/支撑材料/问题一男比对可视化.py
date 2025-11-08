import matplotlib.pyplot as plt
import numpy as np

# 设置字体以支持微符号
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置默认字体

# 类别统计条形图
category_labels = ['植物油类', '蔬菜、菌藻、水果类', '谷、薯类', '畜、禽、鱼、蛋类及制品', '奶、干豆、坚果、种子类及制品']
category_counts = [8, 7, 6, 4, 2]

plt.figure(figsize=(10, 6))
plt.bar(category_labels, category_counts, color='skyblue')
plt.xlabel('食物类别')
plt.ylabel('数量')
plt.title('食物类别统计')
plt.tight_layout()
plt.show()

# 实际摄入量与推荐摄入量比较条形图
labels = ['蛋白质 (g)', '脂肪 (g)', '碳水化合物 (g)', '钙 (mg)', '铁 (mg)', '锌 (mg)',
          '维生素A (ug)', '维生素B1 (mg)', '维生素B2 (mg)', '维生素C (mg)']
actual_values = [75.3315, 125.38, 293.31, 578.5, 18.773, 9.986, 518.4, 1.46, 1.267, 40.96]
recommended_values = [60, 80, 300, 800, 12, 12.5, 800, 1.4, 1.4, 100]

x = np.arange(len(labels))
width = 0.35

fig, ax = plt.subplots(figsize=(14, 8))
rects1 = ax.bar(x - width/2, actual_values, width, label='实际摄入量', color='skyblue')
rects2 = ax.bar(x + width/2, recommended_values, width, label='推荐摄入量', color='lightgreen')

ax.set_xlabel('营养素种类')
ax.set_ylabel('摄入量')
ax.set_title('实际摄入量与推荐摄入量比较')
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45)
ax.legend()

fig.tight_layout()
plt.show()

# 宏量营养素能量占比饼图
labels = ['蛋白质能量占比', '脂肪能量占比', '碳水化合物能量占比']
sizes = [11.58, 43.35, 45.07]
colors = ['#ff9999','#66b3ff','#99ff99']
explode = (0.1, 0, 0)  # "explode" the 1st slice

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
        shadow=True, startangle=140)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.title('宏量营养素能量占比')
plt.show()

# 每餐能量占总能量的百分比条形图
meal_labels = ['早餐', '午餐', '晚餐']
meal_energy_percentages = [30.253140, 37.680034, 32.066826]

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(meal_labels, meal_energy_percentages, color='skyblue')

ax.set_xlabel('用餐时间')
ax.set_ylabel('能量占比 (%)')
ax.set_title('每餐能量占总能量的百分比')

fig.tight_layout()
plt.show()

# 必需氨基酸评分条形图
amino_acid_labels = ['异亮氨酸', '亮氨酸', '赖氨酸', '含硫氨基酸', '芳香族氨基酸', '苏氨酸', '色氨酸', '缬氨酸']
amino_acid_scores = [53.17, 51.45, 47.00, 40.16, 43.99, 44.74, 53.86, 48.79]

plt.figure(figsize=(10, 6))
plt.bar(amino_acid_labels, amino_acid_scores, color='skyblue')
plt.axhline(y=60, color='r', linestyle='--', label='合理下限')
plt.axhline(y=80, color='g', linestyle='--', label='比较合理下限')
plt.xlabel('必需氨基酸')
plt.ylabel('评分')
plt.title('必需氨基酸评分（AAS）')
plt.legend()
plt.tight_layout()
plt.show()

# 第一限制氨基酸条形图
labels = ['第一限制氨基酸', '第一限制氨基酸评分']
values = ['含硫氨基酸', 40.16]

fig, ax = plt.subplots(figsize=(8, 6))
rects = ax.bar(labels, [0, 40.16], color=['skyblue', 'lightgreen'])

ax.set_xlabel('氨基酸种类')
ax.set_ylabel('评分')
ax.set_title('第一限制氨基酸评分')

fig.tight_layout()
plt.show()
