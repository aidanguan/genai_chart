"""最终调试：检查整个数据流"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.generate_service import GenerateService
import json

async def test():
    service = GenerateService()
    user_text = "方案1：优势是价格便宜，但是质量差。方案2：优势是质量好，但是价格贵。"
    template_id = "compare-hierarchy-left-right"
    
    print("=" * 80)
    print("步骤1：调用 extract_data")
    print("=" * 80)
    
    result = await service.extract_data(
        user_text=user_text,
        template_id=template_id,
        force_provider='system'
    )
    
    print("\n步骤2：检查返回的 config.data.items")
    print("=" * 80)
    
    items = result.get('config', {}).get('data', {}).get('items', [])
    
    for i, item in enumerate(items):
        print(f"\n根节点{i+1}:")
        print(f"  label: {item.get('label')}")
        print(f"  children数量: {len(item.get('children', []))}")
        for j, child in enumerate(item.get('children', [])):
            print(f"    Child{j+1}: label='{child.get('label')}', desc='{child.get('desc')}'")
    
    print("\n\n步骤3：完整的 config.data")
    print("=" * 80)
    print(json.dumps(result.get('config', {}).get('data'), indent=2, ensure_ascii=False))
    
if __name__ == '__main__':
    asyncio.run(test())
