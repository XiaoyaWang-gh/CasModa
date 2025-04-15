import backoff
import logging
import openai
import requests
import json
import re

KEY = "lUMHwhghyPnB7XhvDd21F4868cF64022B0E7Bd7e30E4870a"

# PROXY_URL = "https://api.openai.com"
# PROXY_URL = "https://api.ezchat.top"
PROXY_URL = "https://platform.ezlinkai.com"

logging.getLogger('backoff').addHandler(logging.StreamHandler())
logging.getLogger('backoff').setLevel(logging.ERROR)

STOP_STR = "END_OF_DEMO"


def extract_code_snippet_from_chatgpt(response):
    # 正则表达式模式，匹配以三个反引号 ``` 开始，中间为代码部分，以三个反引号 ``` 结束
    pattern = r"```.*?```"

    # 在回复中查找匹配正则表达式的所有部分
    code_snippets = re.findall(pattern, response, re.DOTALL)

    # 如果找不到代码片段，返回 ["no repair suggestion"]
    if not code_snippets:
        return ["no repair suggestion"]

    # 返回提取的代码片段列表
    return code_snippets


class ChatGPTAPI:
    def __init__(self, output_file):
        self.key = KEY
        self.output_file = output_file

    # @backoff.on_exception(backoff.expo,
    #                       (openai.error.RateLimitError,
    #                        openai.error.APIConnectionError,
    #                        openai.error.ServiceUnavailableError))
    def get_suggestions(self, input_prompt, if_extract=False):
        openai.api_key = self.key

        data = {
            'model': 'gpt-4-turbo-2024-04-09',
            'messages': [
                {"role": "system", "content": "You are a proficient and helpful assistant in java testing with JUnit framework."},
                {"role": "user", "content": input_prompt}
            ]
        }

        headers = {
            'Authorization': f"Bearer {KEY}",
            'Content-Type': 'application/json'
        }

        response = requests.post(
            f'{PROXY_URL}/v1/chat/completions', data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            response_json = response.json()
            choices = response_json.get('choices')
            if choices:
                result = response_json['choices'][0]['message']['content']
                # the next line used to delete "END_OF_DEMO"
                final_result = result[:result.rfind("END_OF_DEMO")]
            with open(self.output_file, "a") as tf:
                if if_extract:
                    final_result = extract_code_snippet_from_chatgpt(final_result)[
                        0]
                tf.write(final_result+"\n")
        else:
            print("chatgpt调用出现问题，状态码是：", response.status_code)
            final_result = ""

        return


def main():
    testgpt = ChatGPTAPI("23122902.txt")
    for i in range(10):
        testgpt.get_suggestions("Good morning, how are you?")


if __name__ == "__main__":
    main()
