from .keys import AZURE_KEY_10 as KEY
import time
import openai
import logging
import backoff
import itertools
from timer import timer
import os

logging.getLogger('backoff').addHandler(logging.StreamHandler())
logging.getLogger('backoff').setLevel(logging.ERROR)

STOP_STR = "END_OF_DEMO"

openai.api_type = "azure"
openai.api_base = "https://icsoft.openai.azure.com/"
openai.api_version = "2022-12-01"


class CodexAPI:
    def __init__(self, output_file):
        self.key = KEY
        self.output_file = output_file
        # self.round_robin = itertools.cycle(seq)

    @backoff.on_exception(backoff.expo,
                          (openai.error.RateLimitError,
                           openai.error.APIConnectionError,
                           openai.error.ServiceUnavailableError))
    # @timer
    def get_suggestions(self,
                        input_prompt,
                        number_of_suggestions=1, max_tokens=500, temperature=1, frequency_penalty=1):
        # openai.api_key = next(self.round_robin)
        openai.api_key = self.key

        start_time = time.perf_counter()
        response = openai.Completion.create(
            engine="code-davinci-002",
            prompt=input_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            n=number_of_suggestions,
            frequency_penalty=frequency_penalty,
            presence_penalty=0,
            # stream=True,
            stop=STOP_STR,
        )
        # suggestions = response['choices']
        result = ""
        if 'choices' in response:
            x = response['choices']
            if len(x) > 0:
                for i in range(0, len(x)):
                    result = x[i]['text']
                    print(f"{i} yaya {result}")
                    # write in to C:/codes/CodeX/CodeX/txt_repo/output/prefix_stage 23.9.21
                    with open(self.output_file, "a") as tf:
                        tf.write(result)

            else:
                result = ''

        end_time = time.perf_counter()
        run_time = end_time - start_time

        return

        # response_completion_tokens = response["usage"]["completion_tokens"]
        if "completion_tokens" in response["usage"]:
            response_completion_tokens = response["usage"]["completion_tokens"]
        else:
            response_completion_tokens = "N/A"

        if "prompt_tokens" in response["usage"]:
            response_prompt_tokens = response["usage"]["prompt_tokens"]
        else:
            response_prompt_tokens = "N/A"

        if "total_tokens" in response["usage"]:
            response_total_tokens = response["usage"]["total_tokens"]
        else:
            response_total_tokens = "N/A"

        return round(run_time, 3), result, response_completion_tokens, response_prompt_tokens, response_total_tokens
