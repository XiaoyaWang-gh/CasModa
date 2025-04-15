"""
File:
    sample_from_evosuite.py

Description:
    从evosuite生成的测试用例中删除一部分，保证和CUTE相同测试类的测试方法相同，作为和CUTE对比3项覆盖率的测试类
    考虑到例外：也就是evosuite也没有生成充足的测试方法，则保留原文件
Author:
    wxy

Date:
    23.10.23

Usage:
    命令行运行

Input Parameters:  
    slim_evosuite_dir: slim-evosuite-tests目录路径
    test_class_name: 测试类名
    test_method_num_should_be: 应当保留的测试方法数量

Output Results:
    slim-evosuite-tests目录下经过slim的测试类
"""
# Test Command:
# python -m sample_from_evosuite C:\dataset\d4j-spec5\1_gson\v-github\gson-master\gson\slim-evosuite-tests\com\google\gson\internal\bind\util ISO8601Utils_ESTest.java 16


from pathlib import Path
import random 
import sys


# Step 1 : 找到EvoSuite生成的特定测试类
# Step 2 : 数出该测试类中现有的test method的数目
# Step 3 : 比对现有数目和应当保留的数目，决定是否要删除，如果无需删除，则打印决定，结束程序，如果需要删除，则进行下一步
# Step 4 : 用随机数生成器，决定生成要删除的test method的id
# Step 5 : 删除对应的test method
# Step 6 : 覆盖重写新的程序

def generate_deleted_id_list(expected_num, actual_num):  
    """
    随机决定删除的id list
    (1) 断言actual_num > expected_num，不满足则抛异常
    (2) 生成的id_list是从[0,actual_num-1]范围的内的正整数中随机抽取actual_num-expected_num个数
    """
    if actual_num <= expected_num:  
        raise ValueError("actual_num must be greater than expected_num.")  
      
    id_list = list(range(actual_num))  
    random.shuffle(id_list)  
      
    deleted_id_list = id_list[:actual_num - expected_num]  
    return deleted_id_list

def override_with_hashtag(str,start,end):
    """
    将字符串的指定位置用#覆盖，保证字符串长度不变，start包括，end不包括
    @return 返回覆盖以后的
    """
    if start >= end:
        raise ValueError("start must be less than end.")
    original_len = len(str)
    new_str = str[:start] + "#"*(end-start) + str[end:]
    new_len = len(new_str)
    assert original_len == new_len
    return new_str

def delete_some_methods(test_class_content, deleted_id_list):
    """
    从测试类中删除特定id的方法，使用num+()作为定界符，向前找到@Test(包含)，向后再找到@Test(不包含)，删除一个方法
    特例：最后一个test method，向后是找不到@Test的，结束位置就定为字符串len-1(记得strip)
    @param : 测试类存进的字符串
    @return : 删除了一些test method的测试类字符串
    """
    print(f"传给delete_some_methods的deleted_id_list为：{deleted_id_list}")
    # 对deleted_id_list进行升序排序
    deleted_id_list.sort()
    print(f"排序后的的deleted_id_list为：{deleted_id_list}")
    for id in deleted_id_list:
        delimiter = str(id)+"()"
        d_idx = test_class_content.find(delimiter) # 定界符的位置
        if d_idx == -1:
            raise ValueError(f"delimiter {d_idx} not found.")
        s_idx = test_class_content.rfind("@Test",0, d_idx) # 向前找到@Test的位置 
        if s_idx == -1:
            raise ValueError(f"@Test {s_idx} not found.")
        e_idx = test_class_content.find("@Test", d_idx) # 向后找到@Test的位置
        if e_idx == -1:
            e_idx = len(test_class_content) - 1
        if s_idx >= e_idx:
            raise ValueError("删除的起始索引必须小于结束索引")
        print(f"d_idx : {d_idx}, s_idx : {s_idx}, e_idx:{e_idx}")
        
        test_class_content = override_with_hashtag(test_class_content, s_idx, e_idx)
        
    # 删除井号
    test_class_content = test_class_content.replace("#","")
    print(test_class_content)
    return test_class_content
    
    
    

def main():
    
    # 读取命令行参数
    if len(sys.argv) != 4:
        print("Usage: python -m sample_from_evosuite <slim_evosuite_dir> <test_class_name> <test_method_num_should_be>")
        exit(1)
    slim_evosuite_dir = Path(sys.argv[1])
    test_class_name = sys.argv[2]
    test_method_num_should_be = int(sys.argv[3])

    # Step 1 : 找到EvoSuite生成的特定测试类
    test_class_file = slim_evosuite_dir / (test_class_name+".java")
    # 存入字符串变量
    with open(test_class_file, "r") as f:
        test_class_content = f.read()
        test_class_content = test_class_content.strip()

    # Step 2 : 数出该测试类中现有的test method的数目，即，数@Test(timeout = 4000)
    test_method_num = test_class_content.count("@Test(timeout = 4000)")

    # Step 3 : 比对现有数目和应当保留的数目
    if test_method_num_should_be >= test_method_num:
        print(f"test_method_num_should_be : {test_method_num_should_be}")
        print(f"test_method_num : {test_method_num}")
        print("test method num is enough less, no need to sample.")
        exit(0)

    # Step 4 : 用随机数生成器，决定生成要删除的test method的id
    deleted_id_list = generate_deleted_id_list(test_method_num_should_be, test_method_num)
    print(f"应当删除的序号列表是：\n{deleted_id_list}")

    # Step 5 : 删除对应的test method
    test_class_content = delete_some_methods(test_class_content, deleted_id_list)

    # Step 6 : 覆盖重写新的程序
    with open(test_class_file, "w") as f:
        f.write(test_class_content)

    print("Done.")
    print(f"测试类{test_class_name}瘦身完毕，删除了{len(deleted_id_list)}个测试方法。")

if __name__ == "__main__":
    main()