# 教程URL https://python-graph-gallery.com/341-python-gapminder-animation/


# Libraries
import pandas as pd
# import matplotlib
import matplotlib.pyplot as plt

data_dict = {
    'assertSame': 8,
    'assertTrue': 831,
    'assertThrows': 14, 
    'assertFalse': 192,
    'assertNotEquals': 99,
    'assertEquals': 2512,
    'assertNull': 71, 
    'assertNotNull': 645,
    'assertNotSame': 32,
    'expect': 680,
    'assertArrayEquals': 158,
    'assertThat': 147, 
    'fail': 138
}

# 将data_dict的key,value都转化为列表
oracle_list = list(data_dict.keys())
num_list = list(data_dict.values())
# 创建一个包含离散值的Series对象  
oracle_type = pd.Series(oracle_list)  
# 将Series对象转换为Categorical类型  
oracle_type_categorical = oracle_type.astype('category')


def main():

    # Set the figure size
    plt.figure(figsize=(10, 10))

    # Scatterplot
    plt.scatter(
        x = oracle_list, 
        y = num_list, 
        s= [float(num)* 5 for num in num_list] , 
        c= oracle_type_categorical.cat.codes, 
        cmap="Accent", 
        alpha=0.6, 
        edgecolors="white", 
        linewidth=2
    )
    
    # Add titles (main and on axis)
    plt.xlabel("JUnit4 Oracle Type")
    plt.ylabel("Number of Oracles")
    plt.title("Distribution of Testing Oracle API Types")
    plt.ylim(0,2800)
    # 设置x轴刻度标签为原始的字符串值  
    plt.xticks(range(len(oracle_list)), oracle_list, rotation=310, ha='left')

    plt.show()

if __name__ == "__main__":
    main()