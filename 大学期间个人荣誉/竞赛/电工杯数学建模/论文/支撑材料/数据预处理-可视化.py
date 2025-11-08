import pandas as pd
import matplotlib.pyplot as plt

# 读取数据
file_path = '数据预处理数据集.xlsx'
data = pd.read_excel(file_path)

# 数据预处理
food_names = data.iloc[:, 0]
protein = data.iloc[:, 1]
calcium = data.iloc[:, 2]
threonine = data.iloc[:, 3]
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用SimHei字体
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号
# 绘制蛋白质含量条形图
plt.figure()
plt.bar(food_names, protein)
plt.title('蛋白质含量 (g/100g)')
plt.xlabel('食物')
plt.ylabel('蛋白质含量 (g/100g)')
plt.xticks(rotation=90)
plt.grid(True)
plt.tight_layout()  # 以适应标签
plt.savefig('protein_content.png')
plt.close()

# 绘制钙含量条形图
plt.figure()
plt.bar(food_names, calcium)
plt.title('钙含量 (mg/100g)')
plt.xlabel('食物')
plt.ylabel('钙含量 (mg/100g)')
plt.xticks(rotation=90)
plt.grid(True)
plt.tight_layout()  # 以适应标签
plt.savefig('calcium_content.png')
plt.close()

# 绘制苏氨酸含量散点图
plt.figure()
plt.scatter(protein, threonine, c='blue', marker='o')
plt.title('蛋白质含量与苏氨酸含量的关系')
plt.xlabel('蛋白质含量 (g/100g)')
plt.ylabel('苏氨酸含量 (mg/g蛋白质)')
plt.grid(True)
plt.savefig('threonine_content_scatter.png')
plt.close()

# 数据描述
print('收集到的数据描述：')
print(f'共有 {data.shape[0]} 种食物，每种食物包含以下信息：')
print('1. 蛋白质含量 (g/100g)')
print('2. 钙含量 (mg/100g)')
print('3. 苏氨酸含量 (mg/g蛋白质)')
print('以下是部分数据预览：')
print(data.head())
