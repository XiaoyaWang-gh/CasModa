'''
source file : 
    - C:\codes\CodeX\vlis7_backup\CodeX_back_to_chatgpt\txt_repo\testbody\query_set\binance\focalname_paralist.txt
    - C:\codes\Java\extract_func_test_pair\src\main\java\org\funcClassMap.json
target file : C:\codes\CodeX\vlis7_backup\CodeX_back_to_chatgpt\txt_repo\validation\binance\testClass_place.json
'''
import os
import json

func_class_map_path = r'C:\codes\Java\extract_func_test_pair\src\main\java\org\funcClassMap.json'
func_class_map = dict()
with open(func_class_map_path,'r') as f:
    json_lst = json.load(f)
    func_class_map = {item['funcname']:item['classname'] for item in json_lst}

focalname_paralist_path = r'C:\codes\CodeX\vlis7_backup\CodeX_back_to_chatgpt\txt_repo\testbody\query_set\binance\focalname_paralist.txt'
focalname_list = []

def turn_signature_into_name(signature):
    tmp = signature.split('(')[0]
    name = tmp.split()[-1]
    return name


with open(focalname_paralist_path,'r') as f:
    focalname_paralist_lst = f.readlines()
    focalname_list = [turn_signature_into_name(signature) for signature in focalname_paralist_lst]
    

'''
json_to_write 
"id_array":[id],
"pro_with_ver": "chart_1f_chart",
"test_class_name": "XXXTest"
'''
json_lst = []
for id,focalname in enumerate(focalname_list):
    test_class_name = func_class_map[focalname]

    one_data = dict()
    one_data["id_array"] = [id+1]
    one_data["pro_with_ver"] = "master"
    one_data["test_class_name"] = test_class_name+'Test'

    json_lst.append(one_data)

target_file = r'C:\codes\CodeX\vlis7_backup\CodeX_back_to_chatgpt\txt_repo\validation\binance\testClass_place.json'

with open(target_file,'w') as f:
    json.dump(json_lst,f)