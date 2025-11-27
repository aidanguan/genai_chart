"""测试Dify API URL"""
import httpx
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def test_url():
    base_url = os.getenv('DIFY_API_BASE_URL')
    api_key = os.getenv('DIFY_API_KEY')
    
    print(f"Base URL: {base_url}")
    print(f"API Key: {api_key[:20]}..." if api_key else "API Key: 未配置")
    
    # 测试几个可能的URL
    urls = [
        f"{base_url}/workflows/run",
        f"{base_url}/workflows/run/",
        f"https://dify-uat.42lab.cn/v1/workflows/run",
    ]
    
    payload = {
        "inputs": {"user_text": "测试"},
        "response_mode": "blocking",
        "user": "test"
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    for url in urls:
        print(f"\n测试URL: {url}")
        try:
            async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
                response = await client.post(url, json=payload, headers=headers)
                print(f"  状态码: {response.status_code}")
                print(f"  响应前200字符: {response.text[:200]}")
        except Exception as e:
            print(f"  错误: {e}")

if __name__ == "__main__":
    asyncio.run(test_url())
