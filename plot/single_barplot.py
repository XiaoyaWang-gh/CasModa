import matplotlib.pyplot as plt
import numpy as np
import os

default_path = r"C:\scire\CUTE_figrues_tables\pdfs"

colors = [
    "#0091EA",
    "#00C853",
    "#AEEA00",
    "#FFAB00",
    "#00E5FF",
    "#00E676",
    "#C6FF00",
    "#FFC400",
    "#18FFFF",
    "#69F0AE",
    "#EEFF41",
    "#FFD740"
]


def plot_bar_chart(label_lst, data_lst, title, y_label, order='original', path=None, color_lst=None):
    """  
    绘制条形图并保存为PDF文件。  

    参数:  
    - label_lst: 字符串数组，与data_lst一一对应的标签列表。  
    - data_lst: 存放若干个浮点数的列表。  
    - title: 图的名称，字符串类型。  
    - y_label: y轴的标签，字符串类型。
    - order: 数据的排序方式，可选值为'original'（默认）、'ascending'和'descending'。  
    - path: 条形图保存的路径，字符串类型。如果为None，则不保存图像。  
    - color_lst: 条形图中每根条柱的颜色列表，可选参数。如果为None，则使用默认颜色。  

    返回值:  
    无返回值。  

    示例用法:  
    plot_bar_chart(['A', 'B', 'C', 'D'], [1.2, 2.5, 0.8, 3.1], "My Bar Chart", order='ascending', path="C:/myplot.pdf", color_lst=['red', 'green', 'blue', 'yellow'])  
    """

    # 根据order参数对数据进行排序
    if order == 'ascending':
        sorted_indices = np.argsort(data_lst)
    elif order == 'descending':
        sorted_indices = np.argsort(data_lst)[::-1]
    else:
        sorted_indices = np.arange(len(data_lst))

    # 根据排序后的索引重新排列标签和数据
    sorted_labels = [label_lst[i] for i in sorted_indices]
    sorted_data = [data_lst[i] for i in sorted_indices]

    # 创建绘图对象
    fig, ax = plt.subplots()

    # 设置字体为"Times New Roman"
    plt.rcParams['font.family'] = 'Times New Roman'

    # 设置条柱的位置
    x_pos = np.arange(len(sorted_data))

    # 绘制条形图
    ax.bar(x_pos, sorted_data, color=color_lst)

    # 设置x轴标签和刻度
    ax.set_xticks(x_pos)
    ax.set_xticklabels(sorted_labels, rotation=30, ha='right')

    # 设置y轴标签
    ax.set_ylabel(y_label)

    # 在条柱上方显示数据
    for i, v in enumerate(sorted_data):
        ax.text(i, v + 0.1, str(v), ha='center', va='bottom')

    # 设置图标题
    ax.set_title(title)

    # 调整子图位置，向右上方移动
    fig.subplots_adjust(left=0.2, bottom=0.2, right=0.8, top=0.8)

    # 保存图像
    # if path is not None:
    #     plt.savefig(path)

    # 显示图像
    plt.show()


def main():
    assertion_type_lst = [
        "assertEquals",
        "assertNotEquals",
        "assertTrue",
        "assertFalse",
        "assertNull",
        "assertNotNull",
        "assertSame",
        "assertNotSame",
        "assertArrayEquals",
        "assertThat",
        "assertThrows",
        "expect",
        "fail"
    ]

    assertion_num_lst = [
        2512, 99, 831, 192, 71, 645, 8, 32, 158, 147, 14, 680, 138
    ]

    title = "assertion_distribution"

    save_path = os.path.join(default_path, title+".pdf")

    plot_bar_chart(assertion_type_lst, assertion_num_lst, title,
                   "num of assertions",
                   "descending", path=save_path, color_lst=colors)


if __name__ == "__main__":
    main()
