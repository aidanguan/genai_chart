"""测试Dify工作流集成"""
import asyncio
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from app.services.generate_service import get_generate_service

# 加载环境变量
load_dotenv()

async def test_dify_call():
    """测试Dify API调用"""
    service = get_generate_service()
    
    # 测试数据
    user_text = "2023年各城市销售额：北京1000万元，上海1200万元，广州800万元，深圳900万元。"
    template_id = "bar-chart-vertical"  # 使用数据库中实际存在的模板
    
    print(f"\n测试用例:")
    print(f"  文本: {user_text}")
    print(f"  模板: {template_id}")
    print(f"\n开始调用数据提取API...")
    
    try:
        result = await service.extract_data(
            user_text=user_text,
            template_id=template_id
        )
        
        print(f"\n✅ 调用成功!")
        print(f"  生成方法: {result.get('generation_method')}")
        print(f"  提取耗时: {result.get('extractionTime')}s")
        
        if 'workflow_info' in result:
            print(f"  工作流信息:")
            print(f"    - 工作流名称: {result['workflow_info'].get('workflow_name')}")
            print(f"    - 工作流运行ID: {result['workflow_info'].get('workflow_run_id')}")
            print(f"    - Dify调用耗时: {result.get('dify_call_time')}s")
        else:
            print(f"  ⚠️  未使用Dify工作流（使用了系统LLM）")
            
        return result
        
    except Exception as e:
        print(f"\n❌ 调用失败: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = asyncio.run(test_dify_call())
    
    # 打印结果摘要
    if result:
        print(f"\n{'='*60}")
        print(f"测试结论:")
        if result.get('generation_method') == 'dify_workflow':
            print(f"  ✅ Dify API调用成功!")
        else:
            print(f"  ⚠️  Dify API未调用，使用了回退机制（系统LLM）")
        print(f"{'='*60}\n")
