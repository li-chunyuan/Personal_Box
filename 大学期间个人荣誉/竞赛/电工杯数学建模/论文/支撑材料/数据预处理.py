import pandas as pd
import numpy as np
import os
import scipy.stats as stats
import matplotlib.pyplot as plt

# 读取Excel数据
file_path = '数据预处理数据集.xlsx'
data = pd.read_excel(file_path)

# 初始化保存结果的变量
results = []

# 创建一个文件夹来保存图像
output_folder = '可视化结果'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 定义一个函数来替换非法文件名字符
def sanitize_filename(filename):
    return "".join(c if c.isalnum() else "_" for c in filename)

for column in data.columns:
    column_data = data[column].dropna()

    # 忽略非数值列
    if not np.issubdtype(column_data.dtype, np.number):
        continue

    # KS检验
    _, p_value = stats.kstest(column_data, 'norm', args=(column_data.mean(), column_data.std()))
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用SimHei字体
    plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号
    # Q-Q图
    plt.figure()
    stats.probplot(column_data, dist="norm", plot=plt)
    plt.title(f'Q-Q Plot for {column}')
    plt.savefig(os.path.join(output_folder, f'QQPlot_{sanitize_filename(column)}.png'))
    plt.close()

    if p_value > 0.05:
        # 数据近似正态分布，使用3σ原则判定异常值
        mu = column_data.mean()
        sigma = column_data.std()
        lower_bound = mu - 3 * sigma
        upper_bound = mu + 3 * sigma
        is_outlier = (column_data < lower_bound) | (column_data > upper_bound)

        # 标记结果
        results.append([column, 'Normal', '3 Sigma Rule'])
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用SimHei字体
        plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号
        # 可视化异常值处理
        plt.figure()
        plt.subplot(1, 2, 1)
        plt.hist(column_data, bins=30, alpha=0.7)
        plt.title(f'Original {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')

        # 剔除异常值
        column_data = column_data[~is_outlier]

        plt.subplot(1, 2, 2)
        plt.hist(column_data, bins=30, alpha=0.7)
        plt.title(f'Processed {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.savefig(os.path.join(output_folder, f'Hist_{sanitize_filename(column)}.png'))
        plt.close()

    else:
        # 数据非正态分布，使用箱型图判定异常值
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用SimHei字体
        plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号
        plt.figure()
        plt.boxplot(column_data)
        plt.title(f'Boxplot for {column}')
        plt.savefig(os.path.join(output_folder, f'Boxplot_{sanitize_filename(column)}.png'))
        plt.close()

        # 箱型图异常值判定
        Q1 = column_data.quantile(0.25)
        Q3 = column_data.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        is_outlier = (column_data < lower_bound) | (column_data > upper_bound)

        # 标记结果
        results.append([column, 'Non-Normal', 'Boxplot Rule'])

        # 可视化异常值处理
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用SimHei字体
        plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号
        plt.figure()
        plt.subplot(1, 2, 1)
        plt.hist(column_data, bins=30, alpha=0.7)
        plt.title(f'Original {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')

        # 剔除异常值
        column_data = column_data[~is_outlier]
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用SimHei字体
        plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号
        plt.subplot(1, 2, 2)
        plt.hist(column_data, bins=30, alpha=0.7)
        plt.title(f'Processed {column} NonNormal')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.savefig(os.path.join(output_folder, f'Hist_{sanitize_filename(column)}_NonNormal.png'))
        plt.close()

    # 更新处理后的数据
    data.loc[~data[column].isna(), column] = column_data

# 保存处理后的数据到新的Excel文件
data.to_excel('处理后的数据集.xlsx', index=False)

# 显示结果
results_df = pd.DataFrame(results, columns=['Column', 'Distribution', 'OutlierMethod'])
print(results_df)
