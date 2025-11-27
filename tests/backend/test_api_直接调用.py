"""直接调用后端API测试"""
import requests
import json

url = "http://localhost:8000/api/v1/generate/extract"

payload = {
    "text": "北京1000万，上海1200万",
    "templateId": "bar-chart-vertical"
}

print("发送请求到:", url)
print("请求数据:", json.dumps(payload, ensure_ascii=False, indent=2))
print("\n等待响应...\n")

response = requests.post(url, json=payload)

print(f"状态码: {response.status_code}")
print(f"\n响应数据:")
data = response.json()
print(json.dumps(data, ensure_ascii=False, indent=2))

print(f"\n生成方法: {data['data'].get('generation_method')}")

if 'workflow_info' in data['data']:
    print(f"工作流信息: {data['data']['workflow_info']}")
else:
    print("未使用Dify工作流")
