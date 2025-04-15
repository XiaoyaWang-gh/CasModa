'''
python -m use_unixcoder
'''
from typing import List
import os
import sys
print(sys.executable)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

import warnings
from transformers import pipeline
from sklearn.cluster import KMeans
from scipy.spatial.distance import cosine
import torch
import numpy as np
from dotenv import load_dotenv

from CUTE_components.models import Prefix_datapoint, Oracle_datapoint, Testcase_datapoint
from CUTE_components.dataset import Prefix_Dataset, Oracle_Dataset, Testcase_Dataset


# 获取当前脚本的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))
# 拼接.env文件的路径
env_path = os.path.join(script_dir, '..', '.env')
# 加载.env文件中的环境变量
load_dotenv(env_path)
# 获取当前测试的项目
pro = os.getenv("DEMO_PRO")


def encode_by_unixcoder(input_str):
    '''
    用unixcoder编码字符串，返回Tensor (1,768)
    '''
    local_path = os.path.join(os.path.dirname(__file__), "localunixcoder")
    extractor = pipeline("feature-extraction", model=local_path)
    output_tensor = extractor(input_str, return_tensors=True)
    # before torch.Size([1, 38, 768])
    final_output = torch.mean(output_tensor, dim=1)  # 第二个维度是序列长度，不确定直接删除对不对
    # after torch.Size([1, 768])
    assert final_output.shape == torch.Size([1, 768])

    return final_output


def cosine_similarity(ts1, ts2):
    '''
    ts1 : Tensor (1,768)
    ts2 : Tensor (1,768)
    计算每个query向量和demo_pool中向量的余弦相似度
    '''
    vector1 = ts1.flatten().numpy()
    vector2 = ts2.flatten().numpy()
    similarity = 1 - cosine(vector1, vector2)

    return similarity  # 取值范围是[-1,1],越大越相似


def most_alike_by_cossimi(query_ts, ts_list):
    '''
    query_ts : Tensor (1,768)
    ts_list : List[(int,str,Tensor)]
    通过余弦相似度，从ts_list中选出和query_ts最相像的ts,返回其index(即元组的第一个元素)
    return: int, float
    '''
    max_similarity = -1
    max_similarity_idx = -1
    for i in range(len(ts_list)):
        idx = ts_list[i]["idx"]
        ts = ts_list[i]["tensor"]
        similarity = cosine_similarity(query_ts, ts)
        if similarity > max_similarity:
            max_similarity = similarity
            max_similarity_idx = idx
    return max_similarity_idx, max_similarity


def sort_by_cossimi(query, samples, reverse=False):
    '''
    query : str
    samples : list(str)  [0.68, 0.26, 0.77, 0.80, 0.25]
    return : list(int)   [2, 1, 3, 4, 0]
    利用余弦相似度，将samples中的元素按照和query相似度升序/降序排序
    返回索引列表
    '''
    query_tensor = encode_by_unixcoder(query)
    sample_tensors = [encode_by_unixcoder(i) for i in samples]
    similarity_list = [cosine_similarity(
        query_tensor, sample_tensor) for sample_tensor in sample_tensors]
    # 使用sorted()函数对数组元素进行升序排列，并返回每个元素的序号
    idx_list = [x for x in range(len(similarity_list))]
    sorted_idx_list = sorted(
        idx_list, key=lambda x: similarity_list[x], reverse=reverse)
    return sorted_idx_list


def prefix_sort_by_cossimi(query_dp, samples, reverse=False):
    '''
    query_dp : Prefix_datapoint
    samples : list(Prefix_datapoint)
    return : list(int)
    利用余弦相似度，将samples中的元素按照和query_dp相似度从大到小排序
    这个方法本质上只是把字符串提取出来，排序还是靠sort_by_cossimi
    '''
    """  
    **Deprecated**: This method is no longer recommended for use.  
    """
    warnings.warn(
        "This method is deprecated and will be removed in future versions.", DeprecationWarning)

    assert isinstance(query_dp, Prefix_datapoint)
    assert all(isinstance(sample, Prefix_datapoint) for sample in samples)

    query_str = query_dp.classname+query_dp.constructor+query_dp.focalname_paralist
    sample_strs = [
        sample.classname+sample.constructor+sample.focalname_paralist for sample in samples]

    idx_list = sort_by_cossimi(query_str, sample_strs, reverse=reverse)

    return idx_list


def oracle_sort_by_cossimi(query_dp, samples, reverse=False):
    '''
    query_dp : Oracle_datapoint
    samples : list(Oracle_datapoint)
    return : list(int)
    利用余弦相似度，将samples中的元素按照和query_dp相似度从大到小排序
    这个方法本质上只是把字符串提取出来，排序还是靠sort_by_cossimi
    '''
    """  
    **Deprecated**: This method is no longer recommended for use.  
    """
    warnings.warn(
        "This method is deprecated and will be removed in future versions.", DeprecationWarning)

    assert isinstance(query_dp, Oracle_datapoint)
    assert all(isinstance(sample, Oracle_datapoint) for sample in samples)

    query_str = query_dp.focalname_paralist+query_dp.test_method
    sample_strs = [
        sample.focalname_paralist+sample.test_method for sample in samples]

    idx_list = sort_by_cossimi(query_str, sample_strs, reverse=reverse)

    return idx_list


def cluster_by_kmeans(tensor_list, cluster_num):
    '''
    tensor_list ： list of Tensor (1,768)
    cluster_num : int
    用kmeans聚类成k个簇，返回k维list
    '''

    # 将tensor_list转化为合法输入
    concatenated_tensor = torch.cat(tensor_list, dim=0)
    numpy_array = concatenated_tensor.numpy()
    print("numpy_array.shape:\n", numpy_array.shape)

    # 执行聚类
    kmeans = KMeans(n_clusters=cluster_num)
    labels = kmeans.fit_predict(numpy_array)  # 输出类似于[4 4 4 2 2 2]，表示每个样本属于哪个簇
    label_list = labels.tolist()  # 转化为int类型的list

    return label_list


def read_unixcoder(tensor_file_path):
    '''
    从文件里面读向量还挺繁琐的，在三个地方用到，所以单独封装一下
    : param file_path : str
    : return : list[tensor]
    '''
    encoded_list = []
    with open(tensor_file_path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            # 对原始字符串[-0.03974078595638275, 0.441280335187912, -1.3046798706054688] 进行处理
            line = line.strip()
            line = line[1:-1]
            num_list = line.split(",")
            value_list = [float(num) for num in num_list]
            # 转化为tensor
            tensor = torch.tensor(value_list).view(1, 768)
            encoded_list.append(tensor)
    return encoded_list


def prefix_diversity_retriever(query_tensor, demo_pool, shot_num):
    '''
    要素齐全：unixcoder编码，聚类，余弦相似度选出每个簇中最相像的，存入list返回
    @param
    query_tensor: Prefix_datapoint 经过编码后的向量
    demo_pool: List[Prefix_datapoint]
    order: str
    shot_num: int
    @return
    candidates: List[Prefix_datapoint]
    demo_similarity_list: List[float]
    '''
    candidates: List[Prefix_datapoint] = []

    # 1. unixcoder编码
    encoded_demo_pool = []
    # 直接读取编码好的
    tensor_file = f"txt_repo\\prefix\\demo_pool\\{pro}\\unixcoder_tensor.txt"
    encoded_demo_pool = read_unixcoder(tensor_file)

    # 2. 聚类
    label_list = cluster_by_kmeans(encoded_demo_pool, shot_num)
    # 根据标签归类
    clustered_2d_list = [[] for _ in range(shot_num)]

    if len(demo_pool) != len(label_list):
        print("prefix_diversity_retriever >> Length mismatch in PREFIX STAGE!!")
        print("Length of demo_pool:", len(demo_pool))
        print("Length of label_list:", len(label_list))
        exit()  # 终止程序

    for i in range(len(label_list)):
        label = label_list[i]
        demo = demo_pool[i]
        # 存入元组是为了计算余弦相似度好调度index
        tmp_dict = dict(idx=i, demo=demo, tensor=encoded_demo_pool[i])
        clustered_2d_list[label].append(tmp_dict)
    # 3. 通过余弦相似度选出每个簇中最相像的元组的index

    candidate_idxs = []  # 最后要返回的demo的索引的list
    demo_similarity_list = []  # 出去以后排序要用
    for clustered_1d_list in clustered_2d_list:
        most_alike_demo_idx, max_similarity = most_alike_by_cossimi(
            query_tensor, clustered_1d_list)
        candidate_idxs.append(most_alike_demo_idx)
        demo_similarity_list.append(max_similarity)
    # 4. 存入list返回
    candidates = [demo_pool[idx] for idx in candidate_idxs]

    return candidates, demo_similarity_list


def oracle_diversity_retriever(query, demo_pool, shot_num):
    '''
    要素齐全：unixcoder编码，聚类，余弦相似度选出每个簇中最相像的，存入list返回
    @param
    query: Prefix_datapoint 经过编码后的向量
    demo_pool: List[Oracle_datapoint]
    order: str
    shot_num: int
    @return
    candidates: List[Oracle_datapoint]
    '''
    candidates: List[Oracle_datapoint] = []
    # 1. unixcoder编码
    encoded_demo_pool = []
    # 直接读取编码好的
    tensor_file = f"txt_repo\\oracle\\demo_pool\\{pro}\\unixcoder_tensor.txt"
    encoded_demo_pool = read_unixcoder(tensor_file)

    # 2. 聚类
    label_list = cluster_by_kmeans(encoded_demo_pool, shot_num)
    # 根据标签归类
    clustered_2d_list = [[] for _ in range(shot_num)]

    if len(demo_pool) != len(label_list):
        print("oracle_diversity_retriever >> Length mismatch in ORACLE STAGE!!")
        print("Length of demo_pool:", len(demo_pool))
        print("Length of label_list:", len(label_list))
        exit()  # 终止程序

    for i in range(len(label_list)):
        label = label_list[i]
        demo = demo_pool[i]
        # 存入元组是为了计算余弦相似度好调度index
        tmp_dict = dict(idx=i, demo=demo, tensor=encoded_demo_pool[i])
        clustered_2d_list[label].append(tmp_dict)
    # 3. 通过余弦相似度选出每个簇中最相像的元组的index
    query_tensor = encode_by_unixcoder(
        query.focalname_paralist+query.test_method)
    candidate_idxs = []  # 最后要返回的demo的索引的list
    demo_similarity_list = []  # 出去以后排序要用
    for clustered_1d_list in clustered_2d_list:
        most_alike_demo_idx, max_similarity = most_alike_by_cossimi(
            query_tensor, clustered_1d_list)
        candidate_idxs.append(most_alike_demo_idx)
        demo_similarity_list.append(max_similarity)
    # 4. 存入list返回
    candidates = [demo_pool[idx] for idx in candidate_idxs]

    return candidates, demo_similarity_list


def testcase_diversity_retriever(query, demo_pool, shot_num):
    '''
    和上面两个方法功能类似，最大的区别在于传入的Testcase_datapoint自身就有向量unix_tensor

    '''
    candidates: List[Testcase_datapoint] = []
    # 1. unixcoder编码
    encoded_demo_pool = [demo.unix_tensor for demo in demo_pool]

    # 2. 聚类
    label_list = cluster_by_kmeans(encoded_demo_pool, shot_num)
    # 根据标签归类
    clustered_2d_list = [[] for _ in range(shot_num)]

    if len(demo_pool) != len(label_list):
        print("Length mismatch in PREFIX STAGE!!")
        print("Length of demo_pool:", len(demo_pool))
        print("Length of label_list:", len(label_list))
        exit()  # 终止程序

    for i in range(len(label_list)):
        label = label_list[i]
        demo = demo_pool[i]
        # 存入元组是为了计算余弦相似度好调度index
        tmp_dict = dict(idx=i, demo=demo, tensor=encoded_demo_pool[i])
        clustered_2d_list[label].append(tmp_dict)
    # 3. 通过余弦相似度选出每个簇中最相像的元组的index
    query_tensor = query.unix_tensor
    candidate_idxs = []  # 最后要返回的demo的索引的list
    demo_similarity_list = []  # 出去以后排序要用
    for clustered_1d_list in clustered_2d_list:
        most_alike_demo_idx, max_similarity = most_alike_by_cossimi(
            query_tensor, clustered_1d_list)
        candidate_idxs.append(most_alike_demo_idx)
        demo_similarity_list.append(max_similarity)
    # 4. 存入list返回
    candidates = [demo_pool[idx] for idx in candidate_idxs]

    return candidates, demo_similarity_list


def main():


    ut_file = ""
    dataset_tobe_encoded = []
    dir_path = r'/Users/bytedance/code/casmodatest/CasModa/txt_repo/testbody/demo_pool/ecommerce'

    ut_file = os.path.join(
        dir_path, "fm_tc_tensor.txt")

    dataset_tobe_encoded = Testcase_Dataset(
        dir_path,
        "classname.txt",
        "constr_sign.txt",
        "focalname_paralist.txt",
        "test_name.txt",
        "fake_test_body.txt",
        "unixcoder_tensor.txt"
    ).parse()

    with open(ut_file, "a", encoding="utf-8") as f:
        cnt = 0
        for dp in dataset_tobe_encoded:
            ut = encode_by_unixcoder(
                dp.classname+dp.constructor+dp.focalname_paralist)  # testbody

            # turn Tensor to list
            ut_str = str(ut.flatten().tolist())
            f.write(ut_str+"\n")
            cnt += 1
            print(f"这是第{cnt}个，还差{len(dataset_tobe_encoded)-cnt}个未编码🔆")


def encode_ecommerce():
    dir_path = r'/Users/bytedance/code/casmodatest/CasModa/txt_repo/testbody/demo_pool/ecommerce'

    dest_file = os.path.join(dir_path, "fm_tc_tensor.txt")
    fm_input_file = os.path.join(dir_path, "focal_method.txt")
    tc_input_file = os.path.join(dir_path, "test_case.txt")
    with open(dest_file, "a", encoding="utf-8") as f:
        with open(fm_input_file, "r", encoding="utf-8") as fm_f:
            fm_list = fm_f.readlines()
        with open(tc_input_file, "r", encoding="utf-8") as tc_f:
            tc_list = tc_f.readlines()
    assert len(fm_list) == len(tc_list)

    for i in range(len(fm_list)):
        cnt = i+1
        fm = fm_list[i].strip()
        tc = tc_list[i].strip()
        ut = encode_by_unixcoder(fm+"  "+tc)  # testbody
        # turn Tensor to list
        ut_str = str(ut.flatten().tolist())
        f.write(ut_str+"\n")
        print(f"这是第{cnt}个，还差{len(fm_list) - cnt}个未编码🔆")



if __name__ == "__main__":
    encode_by_unixcoder("test")
    # encode_ecommerce()
