import matplotlib.pyplot as plt

# Given data from the user
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

# 首先，使用 zip 函数将相应的断言计数和断言类型组合在一起
zipped_lists = zip(assertion_num_lst, assertion_type_lst)

# 然后，使用 sorted 函数进行排序，reverse=True 表示降序排序
sorted_pairs = sorted(zipped_lists, reverse=False)

# 最后，使用 zip(*) 分解成两个列表，一个是排序后的断言计数，另一个是相应的断言类型
assertion_num_lst, assertion_type_lst = zip(*sorted_pairs)


# Create a bar plot similar to the uploaded one
plt.figure(figsize=(10,8))
bars = plt.barh(assertion_type_lst, assertion_num_lst, color='skyblue')

# Add the data labels on the bars
for bar in bars:
    width = bar.get_width()
    label_x_pos = width + 30 # shift the text to the right side of the bar
    plt.text(label_x_pos, bar.get_y() + bar.get_height()/2, str(width), 
             va='center')

# Set the labels and title
# plt.xlabel('Number of Assertions')
# plt.ylabel('Assertion Type')
plt.title('Distribution of Testing Oracle API Types')

# Remove the top and right spines
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# Save the figure
# plt_path = '/mnt/data/assertion_bar_chart.png'
# plt.savefig(plt_path)

# 调整图表边距  
plt.subplots_adjust(left=0.18, right=0.95, top=0.92, bottom=0.08) 

# Display the plot
plt.show()
