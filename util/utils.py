import os
import hashlib
import time
import sys
import javalang
from typing import List

from rank_bm25 import BM25Okapi
from transformers import AutoTokenizer

from CUTE_components.models import Prefix_datapoint, Oracle_datapoint, Testcase_datapoint


vlis7_path_prefix = "/data2/chaoni/xiaoyawang/CodeX/"

PLACE_HOLDER = ''' "<OraclePlaceHolder>"; '''


class Util:

    @staticmethod
    def load_bm_25_prefix(bm_25_cache_dict, cAndF, demoPool: List[Prefix_datapoint]):
        # 和load_bm_25_oracle最大的区别在于test_methods要换成constructor+focal_method(cAndF)
        start_time = time.time()
        how_many_md5hash_conflicts = 0

        for i in range(len(demoPool)):
            dp = demoPool[i]
            cAndF_item = dp.classname + dp.constructor + \
                dp.focalname_paralist + str(i)
            md5hash = hashlib.md5(cAndF_item.encode('utf-8')).hexdigest()

            if md5hash in bm_25_cache_dict:
                how_many_md5hash_conflicts += 1
            else:
                bm_25_cache_dict[md5hash] = dp
            cAndF.append(cAndF_item)

        print("how_many_md5hash_conflicts: ", how_many_md5hash_conflicts)
        bm25 = BM25Okapi(cAndF)

        end_time = time.time()
        print(f"load_bm_25: {end_time - start_time} s")
        print("The size of the bm25 cache is {} bytes".format(
            sys.getsizeof(bm_25_cache_dict)))
        print(f"total entries: {len(bm_25_cache_dict.keys())}")
        return bm25

    @staticmethod
    def load_bm_25_oracle(bm_25_cache_dict, fAndT, demoPool: List[Oracle_datapoint]):
        start_time = time.time()
        how_many_md5hash_conflicts = 0

        for i in range(len(demoPool)):
            dp = demoPool[i]
            ft_item = dp.focalname_paralist+dp.test_method + \
                str(i)  # 匹配datapoint哪些元素之间的相似度是这里决定的
            md5hash = hashlib.md5(ft_item.encode('utf-8')).hexdigest()

            if md5hash in bm_25_cache_dict:
                how_many_md5hash_conflicts += 1
            else:
                bm_25_cache_dict[md5hash] = dp
            fAndT.append(ft_item)

        print("how_many_md5hash_conflicts: ", how_many_md5hash_conflicts)
        bm25 = BM25Okapi(fAndT)

        end_time = time.time()
        print(f"load_bm_25: {end_time - start_time} s")
        print("The size of the bm25 cache is {} bytes".format(
            sys.getsizeof(bm_25_cache_dict)))
        print(f"total entries: {len(bm_25_cache_dict.keys())}")
        return bm25

    @staticmethod
    def load_bm_25_test_method(bm_25_cache_dict, cAndF, demoPool: List[Testcase_datapoint]):
        start_time = time.time()
        how_many_md5hash_conflicts = 0

        for dp in demoPool:
            cAndF_item = dp.constructor+dp.focal_method+dp.test_name
            md5hash = hashlib.md5(cAndF_item.encode('utf-8')).hexdigest()

            if md5hash in bm_25_cache_dict:
                how_many_md5hash_conflicts += 1
            else:
                bm_25_cache_dict[md5hash] = dp
            cAndF.append(cAndF_item)

        print("how_many_md5hash_conflicts: ", how_many_md5hash_conflicts)
        bm25 = BM25Okapi(cAndF)

        end_time = time.time()
        print(f"load_bm_25: {end_time - start_time} s")
        print("The size of the bm25 cache is {} bytes".format(
            sys.getsizeof(bm_25_cache_dict)))
        print(f"total entries: {len(bm_25_cache_dict.keys())}")
        return bm25

    @staticmethod
    def count_codex_tokens(input: str):
        os.environ['CURL_CA_BUNDLE'] = ''
        tk_path = vlis7_path_prefix+"autotokenizer/"
        tokenizer = AutoTokenizer.from_pretrained(tk_path)
        res = tokenizer(input)['input_ids']
        print(f"AutoTokenizer编码后的长度为{len(res)}")
        return len(res)

    # 这个方法是为 insert_oracle 接收到multi-line java code服务的，之前尝试过很多次format并未成功
    # 这个方法并不完善，只能祈祷不遇到字符 ; { }
    def format_java_code(self, java_code: str) -> str:
        result = []
        for char in java_code:
            result.append(char)
            if char in (';', '{', '}'):
                result.append('\n')
        return ''.join(result)

    @staticmethod
    # insert the oracle after last statement, using java parser
    def insert_oracle(java_method_body: str):
        instance = Util()
        # 这三行代码还是过于草率了,需要改进
        formatted_code = instance.format_java_code(java_method_body)

        tokens = javalang.tokenizer.tokenize(
            "class Test { " + formatted_code + " }")
        parser = javalang.parser.Parser(tokens)
        try:
            parser.parse()
            # just insert placeholder aftert the test input
            return formatted_code + PLACE_HOLDER
        except javalang.parser.JavaSyntaxError as e:
            # It means that there are try and loop structure in the test input
            # need to find the first char isn't } with counting down
            for i in range(len(formatted_code)-1, -1, -1):
                if formatted_code[i] != ' ' and formatted_code[i] != '}':
                    return formatted_code[:i+1] + PLACE_HOLDER + formatted_code[i+1:]

    def compact_code(code):
        # 将代码中的所有连续空格替换为一个空格
        code = " ".join(code.split())
        return code


def write_to_file(file_path: str, content: str, mode="a"):
    '''
    这个方法存在的意义是让调用处的写入文件变得更简洁
    file_path : 写入的文件路径地址
    content : 写入的内容
    mode : w or a
    '''
    with open(file_path, mode, encoding="utf-8") as f:
        f.write(content)


def read_to_list(file_path: str):
    '''
    这个方法存在的意义是让调用处的读取文件变得更简洁
    @param
    file_path : 读取的文件路径地址
    @return
    res_list : 读取的内容，以list形式返回
    '''
    with open(file_path, "r", encoding="utf-8") as f:
        read_list = f.readlines()
        res_list = [line.strip() for line in read_list if not line.startswith("-------")]
        return res_list