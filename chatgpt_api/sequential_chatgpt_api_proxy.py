import json
import requests

from util.decorators import retry
from util.strUtils import hascode


KEY = "lUMHwhghyPnB7XhvDd21F4868cF64022B0E7Bd7e30E4870a"

# PROXY_URL = "https://api.ezchat.top"
# PROXY_URL = "https://api.openai.com"
PROXY_URL = "https://api.ezlinkai.com"


@retry(10, delay=5)
def generate_chat_completion(messages):

    data = {
        'model': 'gpt-4-turbo-2024-04-09',
        'messages': messages
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
            answer = result[:result.rfind("END_OF_DEMO")]
    elif '4097 tokens' in response.text:
        messages[1]['content'] = messages[1]['content'][:12000]
        generate_chat_completion(messages)
    else:
        answer = ""
        print("chatgpt调用出现问题 status code is：", response.status_code)
        raise Exception

    return answer


def main():

    initial_messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "按照先后顺序，重复一下我原先问你的所有问题，再进行总结。"}
    ]

    # 输入问题和上下文
    my_messages = [
        {"role": "system", "content": "You are a helpful calendar assistant"},
        {"role": "user", "content": "六月的下一个月有多少天？"},
        {"role": "assistant", "content": "七月有31天。"},
        {"role": "user", "content": "八月有多少天？"},
        {"role": "assistant", "content": "八月也有31天。"},
        {"role": "user", "content": "二月有多少天？"},
        {"role": "assistant", "content": "这要分平年和闰年"},
        {"role": "user", "content": "按照先后顺序，重复一下我原先问你的所有问题和你给我的相应回答。"}
    ]

    # 调用方法进行对话生成
    answer = generate_chat_completion(initial_messages)

    # 打印生成的回答
    print(answer)


if __name__ == "__main__":
    main()
