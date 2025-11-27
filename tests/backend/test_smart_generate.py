import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.services.llm_service import LLMService

async def test_smart_generate():
    """测试智能生成三阶段流程"""
    llm_service = LLMService()
    
    test_text = "我们公司的荣誉体系分为五个等级，金牌会员占比10%，银牌会员占比15%，铜牌会员占比25%，优秀会员占比30%，普通会员占比20%"
    
    print("=" * 80)
    print("测试文本:", test_text)
    print("=" * 80)
    
    # 阶段1: 分类
    print("\n【阶段1: 分类】")
    classification = await llm_service.classify_content(test_text)
    print(f"分类结果: {classification}")
    
    # 阶段2: 模板选择
    print("\n【阶段2: 模板选择】")
    selection = await llm_service.select_template(test_text, classification['type'])
    print(f"选择模板: {selection}")
    
    # 阶段3: 数据提取
    print("\n【阶段3: 数据提取】")
    config = await llm_service.extract_data_for_template(test_text, selection['templateId'])
    print(f"生成配置:")
    
    import json
    print(json.dumps(config, indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 80)
    print("【关键检查】")
    print(f"✓ 模板ID: {selection['templateId']}")
    print(f"✓ 模板名称: {selection['templateName']}")
    print(f"✓ 配置类型: template={config.get('template')}, design={bool(config.get('design'))}")
    print(f"✓ 数据存在: {bool(config.get('data'))}")
    
    # 检查config结构
    if config.get('design'):
        design = config['design']
        print(f"✓ design.structure.type: {design.get('structure', {}).get('type')}")
        print(f"✓ design.items: {design.get('items')}")
    
    if config.get('data'):
        data = config['data']
        print(f"✓ data.title: {data.get('title')}")
        print(f"✓ data.items数量: {len(data.get('items', []))}")
        if data.get('items'):
            print(f"✓ 第一个item: {data['items'][0]}")

if __name__ == '__main__':
    asyncio.run(test_smart_generate())
