"""调试LLM实际响应"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.generate_service import GenerateService
import json

async def debug_llm():
    service = GenerateService()
    
    # 添加一个猴子补丁来拦截LLM响应
    original_call_llm = service._call_llm
    
    async def patched_call_llm(*args, **kwargs):
        result = await original_call_llm(*args, **kwargs)
        print("=" * 80)
        print("LLM原始返回:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("=" * 80)
        return result
    
    service._call_llm = patched_call_llm
    
    user_text = "方案1：优势是价格便宜，但是质量差。方案2：优势是质量好，但是价格贵。"
    template_id = "compare-hierarchy-left-right"
    
    print(f"测试输入: {user_text}")
    print(f"模板ID: {template_id}\n")
    
    result = await service.extract_data(
        user_text=user_text,
        template_id=template_id,
        force_provider='system'
    )
    
    print("\n" + "=" * 80)
    print("最终生成的config:")
    print(json.dumps(result.get('config', {}), indent=2, ensure_ascii=False))

if __name__ == '__main__':
    asyncio.run(debug_llm())
