import backoff
import logging
import openai
import time
KEY = "sess-ssPfMPsSBGdeiuTHZKLGgIzKb57IE5DirkzhDDg9"

logging.getLogger('backoff').addHandler(logging.StreamHandler())
logging.getLogger('backoff').setLevel(logging.ERROR)

STOP_STR = "END_OF_DEMO"


class CodexAPI:
    def __init__(self, output_file):
        self.key = KEY
        self.output_file = output_file

    @backoff.on_exception(backoff.expo,
                          (openai.error.RateLimitError,
                           openai.error.APIConnectionError,
                           openai.error.ServiceUnavailableError))
    
    def get_suggestions(self, input_prompt):
        openai.api_key = self.key

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a proficient and helpful assistant in java testing."},
                {"role": "user", "content": input_prompt}
            ]
        )

        result = response['choices'][0]['message']['content']
        # the next line used to delete "END_OF_DEMO"
        new_result = result[:result.rfind("END_OF_DEMO")]

        with open(self.output_file, "a") as tf:
            tf.write(new_result)

