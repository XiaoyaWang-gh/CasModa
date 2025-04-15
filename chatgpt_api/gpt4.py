from util.strUtils import hascode
from util.decorators import retry
import requests
import json
import os
import openai


KEY = "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"  # 21

# PROXY_URL = "https://api.okkchat.top"
# PROXY_URL = "https://api.ezchat.top"
PROXY_URL = "https://api.openai.com"


@retry(10, delay=5)
def generate_chat_completion(messages):

    data = {
        'model': 'gpt-4',
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
    else:
        answer = ""
        print("chatgpt调用出现问题，状态码是：", response.status_code)
        raise Exception

    return answer


def main():

    pass


if __name__ == "__main__":
    main()
