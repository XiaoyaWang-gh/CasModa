# 这个文件要放到根目录下运行

from CUTE_components.dataset import Prefix_Dataset, Oracle_Dataset, Testcase_Dataset
from util.utils import Util
from mytemplate import prefix_template, oracle_template, testcase_template


project_name = "lang"
prefix_or_oracle = "oracle"
query_or_demo = "query_set"  # "query_set" or "demo_set
long_or_short = "short"  # "long" or "short

window_dict = {"long": "4097_text_window", "short": "2049_text_window"}


vlis7_path_prefix = "/data2/chaoni/xiaoyawang/CodeX/"

TARGET_FILE = f"txt_repo/{prefix_or_oracle}/{query_or_demo}/{project_name}/new_randomOrder_token_count_updated_short.txt"

SWITCH_DICT = {"prefix": 1, "oracle": 2, "testcase": 3}
DEMO_POOL_PATH = {1: f"txt_repo/prefix/{query_or_demo}/{project_name}/",
                  2: f"txt_repo/oracle/{query_or_demo}/{project_name}/",
                  3: f"txt_repo/ablation/testcase/{project_name}/{query_or_demo}/"}


def make_dataset(switch):
    if switch == 1:
        return Prefix_Dataset(
            vlis7_path_prefix+DEMO_POOL_PATH[1],
            "constr_sign.txt",
            "focal_method.txt",
            "test_input.txt",
            "classname.txt",
            "focalname_paralist.txt",
            "testname.txt",
            "passed_token_count.txt"
        )
    elif switch == 2:
        return Oracle_Dataset(
            vlis7_path_prefix+DEMO_POOL_PATH[2],
            "focal_method.txt",
            "330_testMethod_by_randomOrderDemos_updated_short.txt",
            "focalname_paralist.txt",
            "testname.txt",
            "fake_oracle.txt",
            "fake_token_count.txt"
        )
    elif switch == 3:
        return Testcase_Dataset(
            vlis7_path_prefix+DEMO_POOL_PATH[3],
            "focal_method.txt",
            "focalname_paralist.txt",
            "testname.txt",
            "test_body.txt",
            "fake_token_count.txt",
            "classname.txt",
            "constr_sign.txt"
        )
    else:
        raise Exception("switch must be 1 or 2 or 3")


def main():

    switch = prefix_or_oracle

    my_dataset = make_dataset(SWITCH_DICT[switch])

    my_parsed_dataset = my_dataset.new_queryset_parse() # 如果是oracle这里需要选择
    print(f"👑👑 demo_dataset的长度是{len(my_parsed_dataset)}")

    rainbow_ptr = 0
    with open(vlis7_path_prefix+TARGET_FILE, "a") as f:
        for i in range(0, len(my_parsed_dataset), 1):
            pd = my_parsed_dataset[i]
            # 一共有3*2种数token的可能
            if switch == "prefix":
                if query_or_demo == "query_set":
                    token_num = Util.count_codex_tokens(
                        prefix_template.embed_query_template_updated(pd))
                else:
                    token_num = Util.count_codex_tokens(
                        prefix_template.embed_demo_template_updated(pd))
            elif switch == "oracle":
                if query_or_demo == "query_set":
                    token_num = Util.count_codex_tokens(
                        oracle_template.embed_query_template(pd))
                else:
                    token_num = Util.count_codex_tokens(
                        oracle_template.embed_demo_template(pd))
            else:
                if query_or_demo == "query_set":
                    token_num = Util.count_codex_tokens(
                        testcase_template.embed_query_template(pd))
                else:
                    token_num = Util.count_codex_tokens(
                        testcase_template.embed_demo_template(pd))
            f.write(f"{token_num}\n")

            # happy coding trick
            symbols = ['🎆', '🎇', '✨', '🎉', '🎊']
            heart = symbols[rainbow_ptr % 5]
            rainbow_ptr += 1
            print(f"{heart}这是第{i+1}个，还差{len(my_parsed_dataset)-(i+1)}个\n")


if __name__ == "__main__":
    main()
