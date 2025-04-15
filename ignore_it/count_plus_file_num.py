from collections import OrderedDict

from pathlib import Path
from pprint import pprint

path_current = Path.cwd()

PRO_SET = ["cli", "csv", "gson", "chart", "lang"]


def main():
    for pro_name in PRO_SET:
        target_file = path_current / "txt_repo" / \
            "prefix" / "query_set" / (pro_name + "_plus") / "classname.txt"
        class_name_dict = OrderedDict()
        with open(target_file, "r") as f:
            lines = f.readlines()
            lines = [line.strip()
                     for line in lines if not line.strip().startswith("-----")]
        for line in lines:
            class_name = line
            if class_name in class_name_dict:
                class_name_dict[class_name] += 1
            else:
                class_name_dict[class_name] = 1

        pprint(class_name_dict)


if __name__ == "__main__":
    main()
