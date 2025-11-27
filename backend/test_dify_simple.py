"""简单的Dify测试 - 无Unicode问题"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from app.services.dify_workflow_client import get_dify_workflow_client

async def test():
    client = get_dify_workflow_client()
    
    print("\n=== Dify API测试 ===")
    print(f"Base URL: {client.base_url}")
    print(f"API Key: {client.api_key[:20]}...")
    print(f"Timeout: {client.timeout}s")
    
    try:
        result = await client.call_workflow(
            user_text="2023年各城市销售额：北京1000万元，上海1200万元，广州800万元，深圳900万元。",
            template_id="bar-chart-vertical"
        )
        
        print("\n=== SUCCESS ===")
        print(f"Status: {result.get('status')}")
        print(f"Workflow Run ID: {result.get('workflow_run_id')}")
        print(f"Data keys: {list(result.get('data', {}).keys())}")
        return result
        
    except Exception as e:
        print(f"\n=== ERROR ===")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = asyncio.run(test())
