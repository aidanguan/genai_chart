"""检查工作流配置是否正确加载"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from app.services.workflow_mapper import get_workflow_mapper

mapper = get_workflow_mapper()

print("=== 工作流配置检查 ===\n")

# 检查配置文件路径
print(f"配置文件路径: {mapper.config_path}")
print(f"配置文件是否存在: {os.path.exists(mapper.config_path)}\n")

# 检查已加载的映射
print(f"已加载的映射数量: {len(mapper.mappings)}")
print(f"映射的模板: {list(mapper.mappings.keys())}\n")

# 检查几个关键模板
test_templates = ['bar-chart-vertical', 'list-row-horizontal-icon-arrow', 'chart-column-simple']

for template_id in test_templates:
    print(f"\n模板: {template_id}")
    print(f"  是否启用工作流: {mapper.is_workflow_enabled(template_id)}")
    
    config = mapper.get_workflow_config(template_id)
    if config:
        print(f"  工作流配置:")
        print(f"    - workflow_name: {config.get('workflow_name')}")
        print(f"    - enabled: {config.get('enabled')}")
        print(f"    - fallback_to_system_llm: {config.get('fallback_to_system_llm')}")
    else:
        print(f"  无配置")

# 检查环境变量
print(f"\n=== 环境变量检查 ===")
print(f"DIFY_API_BASE_URL: {os.getenv('DIFY_API_BASE_URL')}")
print(f"DIFY_API_KEY: {os.getenv('DIFY_API_KEY')[:20] if os.getenv('DIFY_API_KEY') else 'None'}...")
