from chatgpt_api.codex_api_proxy import ChatGPTAPI
from prompt.prompt_prefix_query import PrefixPrompt
import hashlib
from util.utils import Util
from CUTE_components.models import Prefix_datapoint
from mytemplate import prefix_template
from CUTE_components.dataset import Prefix_Dataset
from typing import List
import os
import random
import sys

win10_path_prefix = "C:/codes/CodeX/vlis7_backup/CodeX_back_to_chatgpt/"
os.environ['CURL_CA_BUNDLE'] = ''

# MAX_EXPECTED_DEMO_LENGTH = 666

# MAX_TOKENS = 2049  # 8193

pname = "cli"
query_num_dict = {"gson": 129, "cli": 255,
                  "csv": 202, "chart": 989, "lang": 1215}
long_or_short = "short"  # "long" or "short
window_dict = {"long": "4097_text_window", "short": "2049_text_window"}
order_dict = {"0": "random", "1": "reverse"}

my_order = "1"  # my_order = sys.argv[1]
shot_dir = "shot_5"  # shot_dir = "shot_" + sys.argv[2]
RETRIEVED_DEMO_NUM = 5  # int(sys.argv[2])

OUTPUT_FILE = f"txt_repo/gpt_output/{pname}/1_prefix_stage/{shot_dir}/{order_dict[my_order]}/CUTE_prefix.txt"
# DEMO_NUMBERI_FILE = f"txt_repo/upd_scp_output/{pname}/5_demo_number/{window_dict[long_or_short]}/{shot_dir}/demonumber_when_testInput_randomOrder.txt"


# step 2-1 使用BM25算法检索出若干个demos for prefix
def bm25_retrived_demos4prefix(query: Prefix_datapoint, demoPool: List[Prefix_datapoint], order: str, shot_num: int) -> List[Prefix_datapoint]:
    # 和bm25_retrived_demos4oracle最大的区别在于test_methods要换成constructor+focal_method
    bm_25_cache_dict = {}
    cAndF = []
    bm25 = Util.load_bm_25_prefix(bm_25_cache_dict, cAndF, demoPool)

    inner_query = query.classname + query.constructor + query.focalname_paralist
    results_top_n = bm25.get_top_n(inner_query, cAndF, n=shot_num)

    candidate_demonstrations: List[Prefix_datapoint] = []

    for r in results_top_n:  # results_top_n是排序后的cAndF
        md5hash_of_query = hashlib.md5(r.encode('utf-8')).hexdigest()

        if md5hash_of_query in bm_25_cache_dict:
            dp = bm_25_cache_dict[md5hash_of_query]
            candidate_demonstrations.append(dp)
        else:
            raise Exception("ah oh, key missing in the dict")
    if order == "random":
        random.Random(330).shuffle(candidate_demonstrations)
    elif order == "reverse":
        candidate_demonstrations.reverse()

    return candidate_demonstrations


# step 3 构建prompt
def get_prefix_prompt(demos: List[Prefix_datapoint], query: Prefix_datapoint) -> str:
    prompt = PrefixPrompt(demos, query)
    return prompt.construct_prompt()


# step 4 将prompt送进CodeX
def gpt_invoke(prompt: str) -> object:
    codex = CodexAPI(OUTPUT_FILE)
    return codex.get_suggestions(prompt)

# def scp_invoke(model,prompt: str):
#     model.generate(prompt)


def main():

    # step 0 : get query set
    QUERY_SET_PATH = f"txt_repo/prefix/query_set/{pname}/"
    query_dataset = Prefix_Dataset(
        win10_path_prefix+QUERY_SET_PATH,
        "constr_sign.txt",
        "focal_method.txt",
        "fake_test_input.txt",  # 这个文件里面全空 test input是第一阶段要生成的
        "classname.txt",
        "focalname_paralist.txt",
        "testname.txt",
        "new_token_count.txt"
    )
    querySet: List[Prefix_datapoint] = []
    querySet = query_dataset.parse()

    # step 1
    DEMO_POOL_PATH = f"txt_repo/prefix/demo_pool/{pname}/"
    demo_dataset = Prefix_Dataset(
        win10_path_prefix+DEMO_POOL_PATH,
        "constr_sign.txt",
        "focal_method.txt",
        "test_input.txt",
        "classname.txt",
        "focalname_paralist.txt",
        "testname.txt",
        "new_token_count.txt"
    )

    # 防止重复加载model
    # model = StarCoderPlusModel(OUTPUT_FILE)

    assert len(querySet) == query_num_dict[pname]

    rainbow_ptr = 0
    # for i in []: # 候补代码
    for i in range(170, len(querySet), 1):  # test stage without len(querySet)

        query = querySet[i]
        print('*' * 100)
        print(f"第{i+1}个被测方法是: {query.classname} {query.focalname_paralist} ")

        demoPool: List[Prefix_datapoint] = []
        demoPool = demo_dataset.parse(
            query_id=query.classname+query.focalname_paralist)

        my_order = 1  # sys.argv[1]
        # step 2
        candidate_demos = bm25_retrived_demos4prefix(
            query, demoPool, my_order)  # 0代表随机顺序，1代表倒序
        # step 3
        prompt = get_prefix_prompt(candidate_demos, query)
        # step 4
        gpt_invoke(prompt)

        # 画分割线
        with open(win10_path_prefix+OUTPUT_FILE, "a") as tf:
            # if timeout_flag:
            #     tf.write("TIMEOUT_WITHOUT_RETURN")
            tf.write(f"\n## ABOVE {i+1} th ## \n")

        symbols = ['🤗', '🥰', '🤩', '😎', '😋', '😉', '😄', '😆']
        heart = symbols[rainbow_ptr % 8]
        rainbow_ptr += 1
        print(f"{heart} 以上是第{i+1}个，还差{len(querySet)-(i+1)}个\n")


if __name__ == "__main__":
    main()
