import os
from openai import OpenAI
import json

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"), 
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

messages = [{'role': 'system', 'content': '你是一个数学专家'}]


while True:
    que = input(">>>>")

    messages.append({'role': 'user', 'content': f'{que}'})

    completion = client.chat.completions.create(
        model="qwen-plus", # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=messages
        )
    json_data = json.loads(completion.model_dump_json())
    
    ans = json_data["choices"][0]["message"]["content"]
    messages.append({'role': 'assistant', 'content': f'{ans}'})
    # print(completion.model_dump_json())
    print("AI: ", ans)