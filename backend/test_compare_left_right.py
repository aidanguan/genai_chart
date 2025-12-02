"""
测试 compare-hierarchy-left-right 数据生成
"""
import asyncio
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.generate_service import GenerateService

async def test_compare_left_right():
    """测试左右层级对比数据生成"""
    service = GenerateService()
    
    # 测试用例: 方案对比
    user_text = "方案1的优势是成本低、实施快,劣势是功能有限。方案2的优势是功能强大、扩展性好,劣势是成本高、周期长。"
    template_id = "compare-hierarchy-left-right"
    
    print(f"\n{'='*80}")
    print(f"测试文本: {user_text}")
    print(f"模板ID: {template_id}")
    print(f"{'='*80}\n")
    
    try:
        result = await service.extract_data(
            user_text=user_text,
            template_id=template_id,
            force_provider='system'
        )
        
        config = result['config']
        print("生成的配置:")
        print(json.dumps(config, indent=2, ensure_ascii=False))
        
        print("\n\n数据结构分析:")
        print(f"  - template: {config.get('template')}")
        print(f"  - data.title: {config.get('data', {}).get('title')}")
        print(f"  - data.items 长度: {len(config.get('data', {}).get('items', []))}")
        
        items = config.get('data', {}).get('items', [])
        for i, item in enumerate(items):
            print(f"\n  根节点 {i+1}:")
            print(f"    - label: {item.get('label')}")
            print(f"    - children 长度: {len(item.get('children', []))}")
            
            for j, child in enumerate(item.get('children', [])):
                print(f"      Child {j+1}: label='{child.get('label')}', desc='{child.get('desc')}'")
        
        print(f"\n\n期望结构:")
        print("  - items[0].label = '方案1' (显示在左侧圆圈)")
        print("  - items[1].label = '方案2' (显示在右侧圆圈)")
        print("  - items[0].children[0].label = '优势' (左侧pill按钮)")
        print("  - items[0].children[0].desc = '成本低、实施快' (pill按钮内容)")
        print("  - items[0].children[1].label = '劣势' (左侧pill按钮)")
        print("  - items[1].children[0].label = '优势' (右侧pill按钮)")
        print("  - items[1].children[1].label = '劣势' (右侧pill按钮)")
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_compare_left_right())
