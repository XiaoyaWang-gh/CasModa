import matplotlib.pyplot as plt


def plot_pie_chart(data_dict, title):
    labels = list(data_dict.keys())
    sizes = list(data_dict.values())

    # 定义颜色系列
    colors = [
        '#508D69',
        '#FBEEAC', 
        '#CEDEBD',
        '#F4CE14', 
        '#FFD9C0',
        '#ECF9FF', 
        '#75C2F6', 
        '#F4D160', 
        '#1D5D9B',
        '#F3B664', 
        '#F99417',
        '#F7F1E5', 
        '#675D50'
    ]

    # 绘制饼图
    plt.pie(sizes, labels=labels, colors=colors,
            autopct='%1.1f%%', startangle=90)

    # 设置图形的纵横比为1：1，使得饼图为一个正圆
    plt.axis('equal')

    # 添加图例
    plt.legend()

    # 添加标题
    plt.title(title)

    # 调整图表边距  
    plt.subplots_adjust(left=0.08, right=0.95, top=0.92, bottom=0.08)  

    # 显示图形
    plt.show()


def main():
    data_dict = {
        'assertEquals': 2512,
        'assertSame': 8,
        'assertTrue': 831,
        'assertThrows': 14, 
        'assertFalse': 192,
        'assertNotEquals': 99, 
        'assertNull': 71, 
        'assertNotNull': 645,
        'assertNotSame': 32,
        'expect': 680,
        'assertArrayEquals': 158,
        'assertThat': 147, 
        'fail': 138
    }
    title = ""  # repair times statistics
    plot_pie_chart(data_dict, title)


if __name__ == "__main__":
    main()
