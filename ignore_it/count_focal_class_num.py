class_file = "C:/codes/CodeX/CodeX/txt_repo/prefix/query_set/gson/classname.txt"


def main():
    with open(class_file, 'r') as f:
        class_list = f.readlines()
        # turn list to set
        class_set = set(class_list)
        # turn set to list
        class_list = list(class_set)
        print(f"共有{len(class_list)}个类,它们分别是")
        for i in class_list:
            print(i)


if __name__ == '__main__':
    main()
