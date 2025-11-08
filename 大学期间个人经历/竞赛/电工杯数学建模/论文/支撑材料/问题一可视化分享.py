import matplotlib.pyplot as plt

# 实际摄入量与推荐摄入量
actual_intake = {
    '蛋白质 (g)': 59.7075,
    '脂肪 (g)': 52.23,
    '碳水化合物 (g)': 272.47,
    '钙 (mg)': 358.25,
    '铁 (mg)': 12.209,
    '锌 (mg)': 7.893,
    '维生素A (ug)': 328.4,
    '维生素B1 (mg)': 1.333,
    '维生素B2 (mg)': 0.9765,
    '维生素C (mg)': 4.76
}

recommended_intake = {
    '蛋白质 (g)': 60,  # 15% of 2400 kcal (60g protein)
    '脂肪 (g)': 80,    # 30% of 2400 kcal (80g fat)
    '碳水化合物 (g)': 300,  # 65% of 2400 kcal (300g carb)
    '钙 (mg)': 800,
    '铁 (mg)': 12,
    '锌 (mg)': 12.5,
    '维生素A (ug)': 800,
    '维生素B1 (mg)': 1.4,
    '维生素B2 (mg)': 1.4,
    '维生素C (mg)': 100
}

# 绘制比较图表
labels = actual_intake.keys()
actual_values = actual_intake.values()
recommended_values = recommended_intake.values()

x = range(len(labels))
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用SimHei字体
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号
plt.figure(figsize=(14, 8))

plt.bar(x, actual_values, width=0.4, label='实际摄入量', align='center')
plt.bar(x, recommended_values, width=0.4, label='推荐摄入量', align='edge')

plt.xlabel('营养素种类')
plt.ylabel('摄入量')
plt.title('实际摄入量与推荐摄入量比较')
plt.xticks(x, labels, rotation=45)
plt.legend()

plt.tight_layout()
plt.show()
