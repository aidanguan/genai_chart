"""测试AiHubMix API调用"""
import openai
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

api_key = os.getenv("AIHUBMIX_API_KEY")
base_url = os.getenv("AIHUBMIX_BASE_URL")

print(f"API Key: {api_key[:25]}...")
print(f"Base URL: {base_url}")

client = openai.OpenAI(
    api_key=api_key,
    base_url=base_url
)

print("\n测试1: 不带reasoning_effort参数")
try:
    response = client.chat.completions.create(
        model="gpt-5.1",
        messages=[
            {"role": "user", "content": "Hello, how are you?"}
        ],
        temperature=0.7
    )
    print("成功！响应:", response.choices[0].message.content[:100])
except Exception as e:
    print("失败:", e)

print("\n测试2: 带reasoning_effort参数（官方文档推荐）")
try:
    response = client.chat.completions.create(
        model="gpt-5.1",
        messages=[
            {"role": "user", "content": "Hello, how are you?"}
        ],
        temperature=0.7,
        reasoning_effort="medium"
    )
    print("成功！响应:", response.choices[0].message.content[:100])
except Exception as e:
    print("失败:", e)
