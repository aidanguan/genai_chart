"""测试CORS配置"""
import requests

# 测试从5176端口的跨域请求
headers = {
    "Origin": "http://localhost:5176",
    "Content-Type": "application/json"
}

# OPTIONS 预检请求
print("测试 OPTIONS 预检请求...")
try:
    r = requests.options(
        "http://localhost:8000/api/v1/templates/recommend",
        headers={
            "Origin": "http://localhost:5176",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type"
        }
    )
    print(f"状态码: {r.status_code}")
    print(f"Response Headers: {dict(r.headers)}")
except Exception as e:
    print(f"失败: {e}")

# POST 请求
print("\n测试 POST 请求...")
try:
    r = requests.post(
        "http://localhost:8000/api/v1/templates/recommend",
        json={"text": "测试", "maxRecommendations": 2},
        headers=headers
    )
    print(f"状态码: {r.status_code}")
    print(f"CORS Headers: {r.headers.get('Access-Control-Allow-Origin')}")
except Exception as e:
    print(f"失败: {e}")
