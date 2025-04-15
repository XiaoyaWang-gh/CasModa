from chatgpt_api.keys import PLUS_OPENAI_API_KEY, NEW_PLUS_KEY, PLUS_KEY_3, PLUS_KEY_4
import openai
openai.api_key = NEW_PLUS_KEY


modelList = openai.Model.list()


for d in modelList.data:
    print(d.id)
