"""测试金字塔图生成"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_pyramid_generation():
    """测试金字塔图生成功能"""
    
    # 测试用户输入
    user_text = """
    企业数字化转型的五个关键层级：
    1. 战略创新 - 数据驱动决策，引领行业变革
    2. 智能运营 - AI赋能业务，实现自动化管理
    3. 数据整合 - 打通数据孤岛，建立统一平台
    4. 流程优化 - 数字化核心业务流程和协作
    5. 基础设施 - 构建云计算和网络基础架构
    """
    
    # 1. 先推荐模板
    print("=" * 60)
    print("1. 测试模板推荐")
    print("=" * 60)
    
    recommend_response = requests.post(
        f"{BASE_URL}/api/v1/templates/recommend",
        json={"text": user_text}
    )
    
    print(f"推荐接口状态: {recommend_response.status_code}")
    if recommend_response.status_code == 200:
        recommend_data = recommend_response.json()
        print(f"推荐结果: {json.dumps(recommend_data, indent=2, ensure_ascii=False)}")
    else:
        print(f"错误: {recommend_response.text}")
        return
    
    # 2. 使用金字塔模板生成信息图
    print("\n" + "=" * 60)
    print("2. 测试金字塔图生成")
    print("=" * 60)
    
    generate_response = requests.post(
        f"{BASE_URL}/api/v1/generate/extract",
        json={
            "text": user_text,
            "templateId": "pyramid-layer"
        }
    )
    
    print(f"生成接口状态: {generate_response.status_code}")
    if generate_response.status_code == 200:
        generate_data = generate_response.json()
        print(f"生成配置: {json.dumps(generate_data, indent=2, ensure_ascii=False)}")
        
        # 检查关键字段
        config = generate_data.get("data", {}).get("config", {})
        print("\n" + "=" * 60)
        print("3. 验证配置结构")
        print("=" * 60)
        
        has_design = "design" in config
        has_structure = has_design and "structure" in config["design"]
        has_items = has_design and "items" in config["design"]
        has_data = "data" in config
        
        print(f"✓ 包含 design: {has_design}")
        print(f"✓ 包含 design.structure: {has_structure}")
        print(f"✓ 包含 design.items: {has_items}")
        print(f"✓ 包含 data: {has_data}")
        
        if has_design:
            print(f"\ndesign 内容:")
            print(json.dumps(config["design"], indent=2, ensure_ascii=False))
        
        if has_data:
            print(f"\ndata 内容:")
            print(json.dumps(config["data"], indent=2, ensure_ascii=False))
        
        # 最终验证
        if has_design and has_structure and has_items and has_data:
            print("\n✅ 配置结构完整，应该可以正常渲染！")
        else:
            print("\n❌ 配置结构不完整，可能会渲染失败")
            
    else:
        print(f"错误: {generate_response.text}")

if __name__ == "__main__":
    test_pyramid_generation()
