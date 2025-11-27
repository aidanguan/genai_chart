"""直接测试Dify调用（绕过服务器）"""
import sys
import os
import asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

async def main():
    from app.services.generate_service import GenerateService
    from app.services.workflow_mapper import get_workflow_mapper
    
    # 检查WorkflowMapper状态
    mapper = get_workflow_mapper()
    print("=== WorkflowMapper状态 ===")
    print(f"配置文件路径: {mapper.config_path}")
    print(f"映射数量: {len(mapper.mappings)}")
    print(f"模板列表: {list(mapper.mappings.keys())}\n")
    
    template_id = "bar-chart-vertical"
    print(f"模板 '{template_id}' 的工作流状态:")
    print(f"  - 是否启用: {mapper.is_workflow_enabled(template_id)}")
    print(f"  - 配置: {mapper.get_workflow_config(template_id)}\n")
    
    # 测试生成
    service = GenerateService()
    user_text = "北京1000万，上海1200万"
    
    print(f"=== 测试数据提取 ===")
    print(f"文本: {user_text}")
    print(f"模板: {template_id}\n")
    
    try:
        result = await service.extract_data(
            user_text=user_text,
            template_id=template_id
        )
        
        print("SUCCESS! 调用成功!")
        print(f"  生成方法: {result.get('generation_method')}")
        
        if 'workflow_info' in result:
            print(f"  工作流ID: {result['workflow_info'].get('workflow_run_id')}")
            print(f"  工作流名称: {result['workflow_info'].get('workflow_name')}")
        else:
            print("  WARNING: 未使用Dify工作流（使用了system_llm）")
        
        print(f"\n数据: {result['config']['data']}")
        
    except Exception as e:
        print(f"ERROR: 调用失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
