# 4.3 晚上完成
from CUTE_components.models import Testcase_datapoint
from typing import List
from util.utils import Util
import hashlib
import random
from prompt.prompt_testbody_query import TestCasePrompt
from chatgpt_api.codex_api import CodexAPI
from CUTE_components.dataset import Testcase_Dataset

MAX_EXPECTED_DEMO_LENGTH = 1000
RETRIEVED_DEMO_NUM = 30
MAX_TOKENS = 4097

OUTPUT_FILE = "txt_repo/ablation/testcase/gson/output/testbody_byRandomOrderDemos.txt"


def bm25_retrived_demos4testbody(query: Testcase_datapoint, demoPool: List[Testcase_datapoint], order=1) -> List[Testcase_datapoint]:

    bm_25_cache_dict = {}
    cAndF = []
    bm25 = Util.load_bm_25_test_method(bm_25_cache_dict, cAndF, demoPool)

    inner_query = query.constructor + query.focal_method + query.test_name
    results_top_n = bm25.get_top_n(inner_query, cAndF, n=RETRIEVED_DEMO_NUM)

    length_of_query = query.token_count  # 更快，最重要的是：更准
    length_of_completion = MAX_EXPECTED_DEMO_LENGTH
    max_demo_length = MAX_TOKENS - (length_of_query+length_of_completion)

    candidate_demonstrations: List[Testcase_datapoint] = []
    length_so_far = 0

    for r in results_top_n:  # results_top_n是排序后的cAndF
        md5hash_of_query = hashlib.md5(r.encode('utf-8')).hexdigest()

        if md5hash_of_query in bm_25_cache_dict:
            dp = bm_25_cache_dict[md5hash_of_query]
            if length_so_far + dp.token_count <= max_demo_length:
                candidate_demonstrations.append(dp)
                length_so_far += dp.token_count
            else:
                print(f"length so far has eventually been {length_so_far}")
                # 此处决定正序(1)还是随机序(0)
                if order == 0:
                    random.Random(330).shuffle(candidate_demonstrations)
                break
        else:
            raise Exception("ah oh, key missing in the dict")

    print("number of testcase candidate demonstrations: ",
          len(candidate_demonstrations))
    return candidate_demonstrations


def tmp_get_testcase_prompt(demos: List[Testcase_datapoint], query: Testcase_datapoint):
    prompt = TestCasePrompt(demos, query)
    return prompt.construct_prompt()


def invoke(prompt: str) -> object:
    codex = CodexAPI(OUTPUT_FILE)
    return codex.get_suggestions(prompt, number_of_suggestions=1, max_tokens=MAX_EXPECTED_DEMO_LENGTH-50, temperature=0, frequency_penalty=1)


def main3():

    QUERY_SET_PATH = "txt_repo/ablation/testcase/gson/query_set/"
    query_dataset = Testcase_Dataset(
        QUERY_SET_PATH,
        "focal_method.txt",
        "focalname_paralist.txt",
        "testname.txt",
        "fake_test_body.txt",
        "token_count.txt",
        "classname.txt",
        "constr_sign.txt"
    )

    querySet = query_dataset.parse()
    assert len(querySet) == 222  # just for gson~!

    DEMO_SET_PATH = "txt_repo/ablation/testcase/gson/demo_pool/"
    demo_dataset = Testcase_Dataset(
        DEMO_SET_PATH,
        "focal_method.txt",
        "focalname_paralist.txt",
        "testname.txt",
        "test_body.txt",
        "token_count.txt",
        "classname.txt",
        "constr_sign.txt"
    )

    rainbow_ptr = 0
    for i in range(46, 48, 1):  # len(querySet)

        query = querySet[i]
        print('*' * 100)
        print(f"第{i+1}个被测方法是: {query.classname} {query.focalname_paralist} ")

        demoPool = demo_dataset.parse(
            query_id=query.classname+query.focalname_paralist)

        candidate_demos = bm25_retrived_demos4testbody(
            query, demoPool, 0)

        prompt = tmp_get_testcase_prompt(candidate_demos, query)

        invoke(prompt)

        # 画分割线
        with open(OUTPUT_FILE, "a") as tf:
            tf.write(f"## ABOVE {i+1} th ## \n")

        symbols = ['🤗', '🥰', '🤩', '😎', '😋', '😉', '😄', '😆']
        heart = symbols[rainbow_ptr % 8]
        rainbow_ptr += 1
        print(f"{heart} 以上是第{i+1}个，还差{len(querySet)-(i+1)}个\n")


if __name__ == "__main__":
    main3()
