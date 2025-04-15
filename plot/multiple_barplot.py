import matplotlib.pyplot as plt
import numpy as np

# 定义颜色系列
colors = ['#FFDBAA', '#FFB7B7',
          '#96C291', '#F4EEEE']
colors2 = ['#F6F1F1', '#AFD3E2', '#19A7CE', '#146C94']


def plot_bar_chart(data_list, title):
    labels = []
    values_A = []
    values_B = []
    # values_C = []
    # values_D = []

    # 提取数据
    for data in data_list:
        for key, value_dict in data.items():
            labels.append(key)
            values_A.append(value_dict['CUTE_gpt3.5_att6'])
            values_B.append(value_dict['EvoSuite'])
            # values_C.append(value_dict['ChatUniTest'])
            # values_D.append(value_dict['CUTE'])

    # 设置柱状图的位置
    x = np.arange(len(labels))
    width = 0.2

    # 绘制柱状图
    fig, ax = plt.subplots()
    ax.bar(x - width, values_A, width, label='CUTE_gpt3.5_att6', color=colors2[0])
    ax.bar(x, values_B, width, label='EvoSuite', color=colors2[1])
    # ax.bar(x + 2 * width, values_C, width,
    #        label='ChatUniTest', color=colors2[2])
    # ax.bar(x + width, values_D, width, label='CUTE', color=colors2[3])

    # 添加刻度标签和图例
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    # 添加标题
    plt.title(title)

    # 显示图形
    plt.show()


def main():
    mc_list = [ # method coverage
        {"cli": {'CUTE_gpt3.5_att6': 82.54, 'EvoSuite': 97.24}},
        {"csv": {'CUTE_gpt3.5_att6': 86.29, 'EvoSuite': 94.05}},
        {"gson": {'CUTE_gpt3.5_att6': 88.98, 'EvoSuite': 93.51}},
        {"chart": {'CUTE_gpt3.5_att6': 91.03, 'EvoSuite': 93.01}},
        {"lang": {'CUTE_gpt3.5_att6': 87.4, 'EvoSuite': 96.77}},
        {"average": {
            'CUTE_gpt3.5_att6': 88.16, 'EvoSuite': 95.00}}
    ]


    lc_list = [ # line coverage
        {"cli": {'CUTE_gpt3.5_att6': 56.47, 'EvoSuite': 81.77}},
        {"csv": {'CUTE_gpt3.5_att6': 56.7, 'EvoSuite': 92.33}},
        {"gson": {'CUTE_gpt3.5_att6': 64.88, 'EvoSuite': 83.66}},
        {"chart": {'CUTE_gpt3.5_att6': 56.92, 'EvoSuite': 77.3}},
        {"lang": {'CUTE_gpt3.5_att6': 65.75, 'EvoSuite': 88.69}},
        {"average": {
            'CUTE_gpt3.5_att6': 61.39, 'EvoSuite': 84.57}}
    ]

    bc_list = [ # branch coverage
        {"cli": {'CUTE_gpt3.5_att6': 42.88, 'EvoSuite': 70.32}},
        {"csv": {'CUTE_gpt3.5_att6': 40.08, 'EvoSuite': 80.95}},
        {"gson": {'CUTE_gpt3.5_att6': 46.23, 'EvoSuite': 68.6}},
        {"chart": {'CUTE_gpt3.5_att6': 44.65, 'EvoSuite': 61.42}},
        {"lang": {'CUTE_gpt3.5_att6': 47.16, 'EvoSuite': 77.41}},
        {"average": {
            'CUTE_gpt3.5_att6': 45.23, 'EvoSuite': 71.44}}
    ]


    plot_bar_chart(bc_list, "branch coverage")


if __name__ == "__main__":
    main()
