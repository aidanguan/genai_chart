"""测试不同的Dify API请求格式"""
import httpx
import asyncio
import os
import json
from dotenv import load_dotenv

load_dotenv()

async def test_payloads():
    base_url = "https://dify-uat.42lab.cn/v1"
    api_key = os.getenv('DIFY_API_KEY')
    url = f"{base_url}/workflows/run"
    
    print(f"测试URL: {url}")
    print(f"API Key: {api_key}\n")
    
    # 测试不同的payload格式
    payloads = [
        {
            "name": "格式1: inputs对象",
            "data": {
                "inputs": {
                    "user_text": "2023年销售额：北京1000万元"
                },
                "response_mode": "blocking",
                "user": "test"
            }
        },
        {
            "name": "格式2: content字段",
            "data": {
                "inputs": {
                    "content": "2023年销售额：北京1000万元"
                },
                "response_mode": "blocking",
                "user": "test"
            }
        },
        {
            "name": "格式3: query字段",
            "data": {
                "inputs": {
                    "query": "2023年销售额：北京1000万元"
                },
                "response_mode": "blocking",
                "user": "test"
            }
        },
        {
            "name": "格式4: 同时包含content和user_text",
            "data": {
                "inputs": {
                    "content": "2023年销售额：北京1000万元",
                    "user_text": "2023年销售额：北京1000万元"
                },
                "response_mode": "blocking",
                "user": "test"
            }
        }
    ]
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    for payload_test in payloads:
        print(f"\n{'='*60}")
        print(f"测试: {payload_test['name']}")
        print(f"Payload: {json.dumps(payload_test['data'], ensure_ascii=False, indent=2)}")
        print(f"{'='*60}")
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(url, json=payload_test['data'], headers=headers)
                print(f"状态码: {response.status_code}")
                
                if response.status_code == 200:
                    print(f"✅ 成功!")
                    result = response.json()
                    print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)[:500]}")
                else:
                    print(f"❌ 失败")
                    print(f"响应: {response.text[:300]}")
                    
        except Exception as e:
            print(f"❌ 异常: {e}")
        
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(test_payloads())
