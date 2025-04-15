# 该文件的作用是，将最初的A3Test提供的类和方法名，按照类名进行排序，方便后续的统计工作

pname = "gson"

SOURCE_FILE = f"C:/dataset/d4j-spec5/A3Test provided/{pname}/{pname}.txt"
TARGET_FILE = f"C:/dataset/d4j-spec5/A3Test provided/{pname}/sorted_{pname}.txt"


def get_cn(item):
    class_name = item.split(" ")[0]
    return class_name


def main():

    item_list = []

    with open(SOURCE_FILE, "r") as origin_f:
        for line in origin_f:
            if line.startswith("---"):
                pass
            else:
                item_list.append(line)

    item_list.sort()

    with open(TARGET_FILE, "w") as sorted_f:
        cn = "AbstractCategoryItemRenderer"
        for item in item_list:
            if cn != get_cn(item):
                cn = get_cn(item)
                sorted_f.write("--"*100)
                sorted_f.write("\n")
            sorted_f.write(item)


if __name__ == '__main__':
    main()
