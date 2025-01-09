import os
from openai import OpenAI
import json
import time

class ChatBot():
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"), 
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        self.messages = [{'role': 'system', 'content': '你是一个统计学家，请以统计学家的身份思考问题'},
                         {'role': 'system', 'content': '你生成的回答将会在html界面中展示，所以请生成html格式的回答，并保持回答美观'},
                         {'role': 'system', 'content': '请不要在回答的内容里插入图片地址，可以用相关的表情包来代替你想插入的图片'},
                         {'role': 'system', 'content': f'如果已知信息不为空的话，请结合已知信息进行回答'}]


    def reply(self,question,content):
        self.messages.append({'role': 'system', 'content': f'已知信息：{content}'})
        self.messages.append({'role': 'user', 'content': f'{question}'})
        
        start_time = time.time()
        print(start_time)
        completion = self.client.chat.completions.create(
            model="qwen-plus", # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            messages=self.messages
        )
        json_data = json.loads(completion.model_dump_json())
        ans = json_data["choices"][0]["message"]["content"]
        self.messages.append({'role': 'assistant', 'content': f'{ans}'})
        last_time = time.time()-start_time
        print("用时: ",last_time)
        return ans