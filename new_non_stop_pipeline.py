import json
from typing import Dict, Any


def get_json_ctx(pro_name)->Dict[str, Any]:
    key_file = f"/Users/bytedance/code/casmodatest/CasModa/txt_repo/testbody/query_set/{pro_name}/favourite-service/methodMap_0503.json"
    value_file = f"/Users/bytedance/code/github/ecommerce-microservice-backend-app/favourite-service/methods_0405_1.json"

    # 读取key文件
    with open(key_file, 'r') as f:
        key_data = json.load(f)

    # 读取value文件
    with open(value_file, 'r') as f:
        value_data = json.load(f)

    result_dict = dict()

    # 根据key_data中的class_name和method_name，匹配value_data中的className和methodName
    for key_item in key_data:
        class_name = key_item['class_name']
        method_name = key_item['method_name']
        for value_item in value_data:
            if value_item['className'] == class_name and value_item['methodName'] == method_name:
                result_dict[class_name+"-"+method_name] = value_item

    return result_dict

def main():
    pro = "ecommerce"
    ctx_dict = get_json_ctx(pro)
    print(len(ctx_dict))
    print(ctx_dict["FavouriteServiceApplication-main"])

if __name__ == "__main__":
    main()
