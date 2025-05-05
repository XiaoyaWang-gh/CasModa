import json
import os
from typing import Dict, Any

from CUTE_components.models import Ecommerce_query_jsonpoint


def get_json_ctx(pro_name, service_name)->Dict[str, Any]:
    key_file = f"/Users/bytedance/code/casmodatest/CasModa/txt_repo/testbody/query_set/{pro_name}/{service_name}/methodMap_0503.json"
    value_file = f"/Users/bytedance/code/github/ecommerce-microservice-backend-app/{service_name}/methods_0405_1.json"

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

def get_ecommerce_queryset(pro_name, service_name, ctx_dict):
    record_json = f"/Users/bytedance/code/casmodatest/CasModa/txt_repo/testbody/query_set/{pro_name}/{service_name}/methodWTensor_0503.json"
    with open(record_json, 'r') as f:
        record_data = json.load(f)
    query_set = []
    for record_item in record_data:
        query_point = Ecommerce_query_jsonpoint(
            class_name=record_item['class_name'],
            func_name=record_item['method_name'],
            focal_func=record_item['method_declaration'],
            unix_tensor=record_item['unixcoder_tensor'],
            rich_ctx_json=ctx_dict.get(record_item['class_name']+"-"+record_item['method_name'])
        )
        query_set.append(query_point)

    return query_set

def main():
    pro = "ecommerce"
    serv = "favourite-service"
    ctx_dict = get_json_ctx(pro, serv)

    query_set = get_ecommerce_queryset(pro, serv, ctx_dict)
    print(len(query_set))

if __name__ == "__main__":
    main()
