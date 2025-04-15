from chatgpt_api.codex_api_proxy import ChatGPTAPI
from prompt.prompt_oracle_query import OraclePrompt
import hashlib
from util.utils import Util
from CUTE_components.models import Oracle_datapoint
from mytemplate import oracle_template
from CUTE_components.dataset import Oracle_Dataset
from typing import List
import os
import random
import sys
import time

win10_path_prefix = "C:/codes/CodeX/vlis7_backup/CodeX_back_to_chatgpt/"
os.environ['CURL_CA_BUNDLE'] = ''


pname = "chart"

query_num_dict = {"gson": 129, "cli": 255,
                  "csv": 202, "chart": 989, "lang": 1215}

order_dict = {"0": "random", "1": "reverse"}
my_order = "1"  # my_order = sys.argv[1]
shot_dir = "shot_5"  # shot_dir = "shot_" + sys.argv[2]
RETRIEVED_DEMO_NUM = 5  # int(sys.argv[2])

OUTPUT_FILE = f"txt_repo/gpt_output/{pname}/3_oracle_stage/{shot_dir}/{order_dict[my_order]}/CUTE_oracle.txt"
# DEMO_NUMBERI_FILE = f"txt_repo/upd_scp_output/{pname}/5_demo_number/{window_dict[long_or_short]}/{order_dict[my_order]}/3demonumber_genStage2_randomOrder.txt"


# step 2-2 使用BM25算法检索出若干个demos for oracle
def bm25_retrived_demos4oracle(query: Oracle_datapoint, demoPool: List[Oracle_datapoint], order: str, shot_num: int) -> List[Oracle_datapoint]:

    bm_25_cache_dict = {}
    fAndT = []
    bm25 = Util.load_bm_25_oracle(bm_25_cache_dict, fAndT, demoPool)

    inner_query = query.focalname_paralist+query.test_method
    results_top_n = bm25.get_top_n(
        inner_query, fAndT, n=shot_num)

    candidate_demonstrations: List[Oracle_datapoint] = []

    for r in results_top_n:
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


def get_oracle_prompt(demos: List[Oracle_datapoint], query: Oracle_datapoint) -> str:
    prompt = OraclePrompt(demos, query)
    return prompt.construct_prompt()


# step 4 将prompt送进CodeX
def gpt_invoke(prompt: str) -> object:
    codex = CodexAPI(OUTPUT_FILE)
    return codex.get_suggestions(prompt)

# def scp_invoke(model,prompt: str):
#     model.generate(prompt)


def main2():

    QUERY_SET_PATH = f"txt_repo/oracle/query_set/{pname}/"
    query_dataset = Oracle_Dataset(
        win10_path_prefix+QUERY_SET_PATH,
        "focal_method.txt",
        "from_transition_stage/shot_5/reverse/CUTE_testMethod.txt",  # 这个文件每次都要改！！！
        "focalname_paralist.txt",
        "testname.txt",
        "fake_oracle.txt",
        "new_randomOrder_token_count_updated_short.txt"  # 这个文件已经无所谓了~ 行数对的上就行
    )

    querySet: List[Oracle_datapoint] = []
    querySet = query_dataset.new_queryset_parse()

    DEMO_POOL_PATH = f"txt_repo/oracle/demo_pool/{pname}/"
    demo_dataset = Oracle_Dataset(
        win10_path_prefix+DEMO_POOL_PATH,
        "focal_method.txt",
        "test_method.txt",
        "focalname_paralist.txt",
        "test_name.txt",
        "oracle.txt",
        "new_token_count.txt"
    )

    # 与stage1 的不同之处是， stage2 的demo pool 只有一个
    demoPool: List[Oracle_datapoint] = []
    demoPool = demo_dataset.demopool_parse()

    # model = StarCoderPlusModel(OUTPUT_FILE)
    assert len(querySet) == query_num_dict[pname]

    rainbow_ptr = 0
    for i in range(len(querySet)-10, len(querySet), 1):

        query = querySet[i]
        # step 2
        candidate_demos = bm25_retrived_demos4oracle(query, demoPool, 0)
        # step 3
        prompt = get_oracle_prompt(candidate_demos, query)
        # step 4
        gpt_invoke(prompt)

        # 下面到了画分割线环节

        with open(win10_path_prefix+OUTPUT_FILE, "a") as tf:
            tf.write('\n'+f"##ABOVE{i+1}"+'-'*150+'\n')

        symbols = ['🤗', '🥰', '🤩', '😎', '😋', '😉', '😄', '😆']
        heart = symbols[rainbow_ptr % 8]
        rainbow_ptr += 1
        print(f"{heart}这是第{i+1}个，还差{len(querySet)-(i+1)}个\n")


if __name__ == "__main__":
    main2()
