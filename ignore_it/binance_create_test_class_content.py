import os
import json
import fnmatch


'''
将TestXXX.java改写为XXXTest.txt
主要的替代是把测试用例换成<TestMethodPlaceHolder>
'''

source_dir = r'C:\dataset\binance-connector-java\src\test\java\unit'
target_dir = r'C:\codes\CodeX\vlis7_backup\CodeX_back_to_chatgpt\txt_repo\validation\binance\test_class_content'
common_txt = r'C:\codes\CodeX\vlis7_backup\CodeX_back_to_chatgpt\ignore_it\super_test.txt'

complete_table = r'C:\codes\Java\extract_func_test_pair\src\main\java\org\classConstrMap.json'

def extract_import_sentence(test_file):
    # 提取一个测试类中的所有import语句
    import_sen_lst = []
    with open(test_file,'r') as f:
        for line in f:
            clean_line = line.strip()
            if clean_line.startswith('import'):
                import_sen_lst.append(clean_line)
    return import_sen_lst

def main():
    # 读入被测类的完整列表
    with open(complete_table,'r') as f:
        class_map = json.load(f)
    all_class_list = [item['classname'] for item in class_map]
    
    # 读入公共导入语句
    with open(common_txt, 'r') as f:
        common_import = f.read()

    # 开始造test_class_content
    # 配料： classname + common_import
    for classname in all_class_list:
        testfile_name = f'{classname}Test.txt'
        target_path = os.path.join(target_dir,testfile_name)
        with open(target_path,'w') as f:
            f.write(common_import)
            f.write(f'public class {classname}Test<ID>'+'{\n\n')
            f.write('    @Test\n    <TestMethodPlaceHolder>\n\n}')

if __name__ == "__main__":
    main()