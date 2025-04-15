import matplotlib.pyplot as plt


def plot_line_chart(title, data, colors):
    # 创建一个新的图形
    plt.figure()

    # 遍历数据字典的每个键值对
    for key, string in data.items():
        values = [float(value.strip("%")) for value in string.split(" || ")]

        # 根据键值对的索引选择对应的颜色
        color = colors[list(data.keys()).index(key)]

        # 为每条折线选择不同的标记样式
        markers = ['s', '^', 'v', 'p', '*', 'h', 'o', '+']
        marker = markers[list(data.keys()).index(key)]

        # x轴的标签
        x_labels = ['Cli', 'Csv',
                    'Gson', 'Chart', 'Lang', 'All']

        # 绘制折线图
        plt.plot(x_labels, values, marker=marker, label=key, color=color)

    # 添加图标题
    plt.title(title)

    # 添加图例
    plt.legend()

    # 调整图表边距  
    plt.subplots_adjust(left=0.08, right=0.95, top=0.92, bottom=0.08)  

    # 显示图形
    plt.show()


def main():


    rolled_fmc_data = { # 这里的每一行是飞书的每一列
        "CUTE(gpt4.0)": "66.82% || 76.68% || 95.45% || 87.80% || 89.71% || 85.75%",
        "CUTE(gpt3.5)": "58.29% || 69.17% || 63.18% || 76.66% || 84.13% || 77.16%",
        "CUTE(codellama)": "16.43% || 37.00% || 24.09% || 40.59% || 51.47% || 42.29%",
        "CUTE(phind-codellama)": "24.20% || 54.40% || 31.40% || 42.90% || 63.50% || 51.53%",
        "CUTE(deepseek-coder)": "35.00% || 51.20% || 45.00% || 72.10% || 76.40% || 67.17%",
        "AthenaTest": "11.07% || 8.98% || 2.89% || 11.70% || 23.35% || 17.05%",
        "A3Test": "25.19% || 25.73% || 14.09% || 31.30% || 49.50% || 38.79%",
        "ChatUniTest": "38.77% || 44.26% || 23.30% || 39.02% || 39.85% || 39.13%",
    }

    fmc_title = "Accuracy%"

    colors = [
        '#508D69', '#F3B664', '#CEDEBD', 
        '#FFD9C0', '#75C2F6', '#F4D160', 
        '#FBEEAC', '#1D5D9B', '#F99417'
    ]

    plot_line_chart(fmc_title, rolled_fmc_data, colors)


if __name__ == "__main__":
    main()
