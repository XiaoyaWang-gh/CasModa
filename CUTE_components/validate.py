import subprocess
import json
import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

TM_PLACEHOLDER = "<TestMethodPlaceHolder>"
ID_PLACEHOLDER = "<ID>"

# 读入生成的测试方法
pro_name = "cli"
shot_num = 5
order = "reverse"


test_method_path = f"txt_repo/gpt_output/{pro_name}/4_final_stage/shot_{shot_num}/{order}/CUTE_testCase.txt"
validation_dir_path = "txt_repo/validation/"
common_project_to_path = validation_dir_path + "common/pro_with_ver_to_path.json"
testClass_place_path = validation_dir_path + f"{pro_name}/testClass_place.json"
testClass_dir_path = validation_dir_path + f"{pro_name}/test_class_content/"
id_to_num_file = validation_dir_path + f"{pro_name}/id_to_num.txt"

output_dir_path = os.path.join(
    validation_dir_path, pro_name, "output", "shot_"+str(shot_num), order)
bf_output = os.path.join(output_dir_path.replace('/', '\\'), "compile_failed")
tf_output = os.path.join(output_dir_path.replace('/', '\\'), "test_failed")
passed_output = os.path.join(output_dir_path.replace('/', '\\'), "passed.txt")
overall_output = os.path.join(
    output_dir_path.replace('/', '\\'), "overall.txt")


def find_objects_with_id(id, testClass_info_json_list):
    for obj in testClass_info_json_list:
        id_array = obj.get('id_array', [])
        if id in id_array:
            pro_with_ver = obj.get('pro_with_ver')
            test_class_name = obj.get('test_class_name')
            break
    return pro_with_ver, test_class_name


def find_objects_by_pro_with_ver(pro_name, pro_with_ver, json_list):
    for obj in json_list:
        if obj.get("pro_name") == pro_name:
            inner_list = obj.get("information")
            for inner_obj in inner_list:
                if inner_obj.get("pro_with_ver") == pro_with_ver:
                    if inner_obj.get('junit5_exe_cp') is not None:
                        return inner_obj.get("focal_class_path"), inner_obj.get("test_class_path"), inner_obj.get("middle_path"), inner_obj.get('junit5_exe_cp')
                    return inner_obj.get("focal_class_path"), inner_obj.get("test_class_path"), inner_obj.get("middle_path")


def main():

    # 读入CUTE生成的测试方法
    with open(test_method_path, "r") as f:
        test_method_list = f.readlines()

    result_cnt_dict = {"passed": 0, "build_failed": 0, "test_failed": 0}
    compile_failed_id_list = []
    test_failed_id_list = []

    # 读入id_to_num.txt
    num_hash = []
    with open(id_to_num_file, "r") as file:
        for line in file:
            line = line.strip('\n')
            num_hash.append(int(line))

    for id in range(1, len(test_method_list)+1):  # 完整版，则终止于 len(test_method_list)+1
        tmp_method = test_method_list[id-1]
        # print(tmp_method)

        # 读入testClass_place.json，存入到一个list当中，每个list是一个字典类型
        with open(testClass_place_path, "r") as f:
            testClass_info = json.load(f)

        testClass_info_json_list = [dict(item) for item in testClass_info]

        # step1 : 通过pro_with_ver得到所属项目的名称和版本号
        # 再去common_project_to_path中找到对应的路径
        pro_with_ver, test_class_name = find_objects_with_id(
            id, testClass_info_json_list)

        # print('pro_with_ver:', pro_with_ver)
        # print('test_class_name:', test_class_name)

        with open(common_project_to_path, "r") as f:
            common_info = json.load(f)
        common_info_json_list = [dict(item) for item in common_info]

        focal_class_path, test_class_path, middle_path = find_objects_by_pro_with_ver(
            pro_name, pro_with_ver, common_info_json_list)

        # print('focal_class_path:', focal_class_path)
        # print('test_class_path:', test_class_path)

        # step2 : 通过id锁定 test class name 再去 testClass_dir_path 下读取对应的.txt 将其中的"<TestMethodPlaceHolder>";替换掉，形成一个TestIDPlus1.java 存放到generated_by_chatgpt文件夹下
        with open(testClass_dir_path+test_class_name+".txt", "r") as f:
            test_class_content = f.read()

        final_test_class = test_class_content.replace(
            TM_PLACEHOLDER, tmp_method)
        final_test_class = final_test_class.replace(ID_PLACEHOLDER, str(id))
        print("final_test_class : ", final_test_class)

        test_class_save_path = os.path.join(
            test_class_path, middle_path, "generated_by_chatgpt")
        # print("test_class_path : ", test_class_path)
        # print("test_class_save_path : ", test_class_save_path)
        os.makedirs(test_class_save_path, exist_ok=True)
        test_class_save_name = test_class_name+str(id)+".java"

        # print("test_class_save_path : ", test_class_save_path)
        # print("test_class_save_name : ", test_class_save_name)

        with open(test_class_save_path+"/" + test_class_save_name, "w") as f:
            f.write(final_test_class)

        # step3 : 对step1得到的路径以及step2得到的文件作为command的参数，进行编译和执行
        result_flag = "passed"

        # 编译测试类
        classpath = "\"" + focal_class_path + ";" + test_class_path + \
            ";C:\\Libraries\\maven-3.5.0\\lib\\*" + "\" "
        compile_command = "javac -cp " + classpath + \
            test_class_save_path+"\\"+test_class_save_name

        compile_result = subprocess.run(compile_command, shell=True,
                                        capture_output=True, text=True)
        # 检查编译结果
        if compile_result.returncode == 0:
            print("编译成功！")
        else:
            print("编译失败！")
            os.remove(test_class_save_path+"/" + test_class_save_name)
            print("已经删除编译失败的文件：", test_class_save_name)
            result_cnt_dict["build_failed"] += num_hash[id-1]
            compile_result_save_path = os.path.join(
                bf_output, test_class_name+str(id)+".txt")
            os.makedirs(bf_output, exist_ok=True)
            with open(compile_result_save_path, "w", encoding="utf-8") as f:
                f.write("stdout:" + compile_result.stdout)
                f.write("\n\n")
                f.write("stderr:" + compile_result.stderr)
            compile_failed_id_list.append(id)
            continue  # 如果编译失败，就压根不去执行了，直接进行下一个test unit

        # 执行测试类
        execute_command = "java -cp " + classpath + " org.junit.runner.JUnitCore " + \
            middle_path.replace('\\', '.') + \
            ".generated_by_chatgpt."+test_class_name+str(id)

        test_result = subprocess.run(
            execute_command, shell=True, capture_output=True, text=True)

        # 检查执行结果
        if test_result.returncode == 0:
            print("执行成功！")
            with open(passed_output, "a", encoding="utf-8") as f:
                f.write(test_class_save_name+" "+tmp_method)
        else:
            print("执行失败！")
            result_flag = "test_failed"
            test_result_save_path = os.path.join(
                tf_output, test_class_name+str(id)+".txt")
            os.makedirs(tf_output, exist_ok=True)
            with open(test_result_save_path, "w", encoding="utf-8") as f:
                f.write("stdout:" + test_result.stdout)
                f.write("\n\n")
                f.write("stderr:" + test_result.stderr)
            test_failed_id_list.append(id)

        result_cnt_dict[result_flag] += num_hash[id-1]

    # 最后把整体的情况写入到overall_output中
    with open(overall_output, "a", encoding="utf-8") as f:
        # 打印整个项目的运行结果
        total = sum(result_cnt_dict.values())

        # 输出每种类型的绝对数量和所占比例
        for key, value in result_cnt_dict.items():
            count = value
            percentage = (count / total) * 100
            f.write(f"{key}: {count} ({percentage:.2f}%)")

        # 输出编译失败的id
        f.write("\n\n")
        f.write("compile_failed_id_list : ")
        for id in compile_failed_id_list:
            f.write(str(id)+" ")

        # 输出测试失败的id
        f.write("\n\n")
        f.write("test_failed_id_list : ")
        for id in test_failed_id_list:
            f.write(str(id)+" ")


# step4 : 如果编译不通过，那么存入编译结果，不再执行，如果执行不通过，存入执行结果，进行下一个test unit
# p.s. 使用一个字典，来记录passed,build falied,test failed这三个类别的个数，最后算出三者各自所占比例
if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    print(f"总耗时: {minutes} min {seconds} sec")
