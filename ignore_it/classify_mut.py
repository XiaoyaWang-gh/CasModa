# 本文件的用途：对methods under test根据所属类进行分类
# 用于:evosuite 逐方法生成测试用例

class_file = "C:/codes/CodeX/CodeX/txt_repo/prefix/query_set/gson/classname.txt"
method_file = "C:/codes/CodeX/CodeX/txt_repo/prefix/query_set/gson/focalname_paralist.txt"

# 我需要这样一个数据结构：一个字典，字典中的每一个元素是从字符串映射到列表的映射
dict4classify = {
    "JsonReader": [],
    "JsonWriter": [],
    "TypeInfoFactory": [],
    "ISO8601Utils": [],
    "UnsafeAllocator": [],
    "ConstructorConstructor": [],
    "$Gson$Types": [],
    "JsonAdapterAnnotationTypeAdapterFactory": [],
    "DefaultDateTypeAdapter": [],
    "ReflectiveTypeAdapterFactory": [],
    "TypeAdapters": [],
    "JsonTreeReader": [],
    "JsonTreeWriter": [],
}


def main():
    with open(class_file, "r") as f:
        class_list = f.readlines()
    with open(method_file, "r") as f:
        method_list = f.readlines()
    for i in range(len(class_list)):
        classname = class_list[i].strip()
        methodname = method_list[i].strip()
        dict4classify[classname].append(methodname)

    for key in dict4classify.keys():
        met_set = set(dict4classify[key])  # 去重嘛
        dict4classify[key] = list(met_set)
        print(key, " : 🎈🎈🎈")
        # 打印得好看一点
        for met in dict4classify[key]:
            print("✨", met)


if __name__ == '__main__':
    main()
