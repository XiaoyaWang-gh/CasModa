"""
File: 
    generate_oracle.py
Description: 
    截取自CUTE_pileline.py
    下半场，针对test_with_only_prefix_file的变异体，生成oracle
Author: 
    wxy
Create Date: 
    2023.12.30
Last Update Date:
    2023.12.30
Usage: 
    设置本文件的global value : pname和attempt后直接在图形界面运行
    设置.env的PROJECT
Input Parameters:  
    (1)项目名称pname
    (2)第多少次跑这个项目attempt-X
Output Files: 
    (1)中间日志文件check_chatgpt_file
    (2)结果文件testcase_file
"""

import os
import logging

from chatgpt_api.sequential_chatgpt_api_proxy import generate_chat_completion



DEFAULT_CHATGPT_ROLE_DICT = {"role": "system", "content": "You are a proficient and helpful assistant in java testing with JUnit4 framework."}

message_list = [ DEFAULT_CHATGPT_ROLE_DICT ]

logger = logging.getLogger(__name__)

def clear_chat_history():
    '''
    重置和chatgpt的历史聊天记录
    '''
    global message_list

    message_list = [ DEFAULT_CHATGPT_ROLE_DICT ]

def call_chatgpt(prompt_str):
    # 提问环节
    one_question = {"role": "user", "content": prompt_str}
    message_list.append(one_question)
    answer = generate_chat_completion(message_list)
    # 善后环节
    one_talk = {"role": "assistant", "content": answer}
    message_list.append(one_talk)
    # 返回结果
    return answer


