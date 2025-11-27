import asyncio
import sys
sys.path.insert(0, 'c:\\AI\\genai_chart-1\\backend')

from app.services.generate_service import get_generate_service

async def test():
    user_text = "我们公司的荣誉体系分为五个等级，金牌会员占比10%，银牌会员占比15%，铜牌会员占比25%，优秀会员占比30%，普通会员占比20%"
    
    service = get_generate_service()
    result = await service.generate_smart(user_text)
    
    print("=" * 80)
    print("智能生成结果:")
    print("=" * 80)
    print(f"\n分类结果: {result['classification']}")
    print(f"\n模板选择: {result['selection']}")
    print(f"\n生成方法: {result['generation_method']}")
    print(f"\n耗时统计: {result['timing']}")
    print(f"\n配置对象:")
    import json
    print(json.dumps(result['config'], ensure_ascii=False, indent=2))

asyncio.run(test())
