import json

INPUT_JSON_FILE = "/Users/bytedance/code/github/ecommerce-microservice-backend-app/user-service/src/resource/funcTestMap.json"  # 待解析的JSON文件路径
METHOD_OUTPUT_FILE = "/Users/bytedance/code/casmodatest/CasModa/txt_repo/testbody/demo_pool/ecommerce/focal_method.txt"  # 存放method值的文件路径
TEST_METHOD_OUTPUT_FILE = "/Users/bytedance/code/casmodatest/CasModa/txt_repo/testbody/demo_pool/ecommerce/test_case.txt"  # 存放testMethod值的文件路径

def parse_and_write_json_data():
    """
    解析JSON文件并将method和testMethod内容分别追加到不同文件
    """
    try:
        # 读取JSON文件
        with open(INPUT_JSON_FILE, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        
        # 检查数据是否为数组
        if not isinstance(data, list):
            raise ValueError("JSON文件内容应该是一个数组")
            
        # 分别打开两个输出文件（使用追加模式'a'）
        with open(METHOD_OUTPUT_FILE, 'a', encoding='utf-8') as method_file, \
             open(TEST_METHOD_OUTPUT_FILE, 'a', encoding='utf-8') as test_method_file:
            
            # 遍历数组中的每个元素
            for item in data:
                if not isinstance(item, dict):
                    continue
                
                # 追加写入method内容
                if 'method' in item:
                    single_line_method = ' '.join(item['method'].splitlines())
                    method_file.write(single_line_method + '\n')
                
                # 追加写入testMethod内容
                if 'testMethod' in item:
                    single_line_test = ' '.join(item['testMethod'].splitlines())
                    test_method_file.write(single_line_test + '\n')
                    
        print(f"数据已成功追加到 {METHOD_OUTPUT_FILE} 和 {TEST_METHOD_OUTPUT_FILE}")
    except FileNotFoundError:
        print(f"错误: 文件 {INPUT_JSON_FILE} 未找到")
    except json.JSONDecodeError:
        print(f"错误: {INPUT_JSON_FILE} 不是有效的JSON文件")
    except Exception as e:
        print(f"发生错误: {str(e)}")


if __name__ == "__main__":
    parse_and_write_json_data()