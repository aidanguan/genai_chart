"""测试后端API接口"""
import requests
import json

BASE_URL = "http://localhost:8000"

# 测试1: 健康检查
print("测试1: 健康检查...")
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"✓ 状态码: {response.status_code}")
    print(f"  响应: {response.json()}")
except Exception as e:
    print(f"✗ 失败: {e}")

# 测试2: 模板推荐
print("\n测试2: 模板推荐...")
try:
    payload = {
        "text": "我想展示一个产品开发的流程，从需求分析到上线部署，总共5个步骤",
        "maxRecommendations": 5
    }
    response = requests.post(
        f"{BASE_URL}/api/v1/templates/recommend",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print(f"✓ 状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"  返回推荐数: {len(data.get('recommendations', []))}")
        print(f"  响应片段: {json.dumps(data, ensure_ascii=False)[:200]}...")
    else:
        print(f"  错误响应: {response.text[:200]}")
except Exception as e:
    print(f"✗ 失败: {e}")
