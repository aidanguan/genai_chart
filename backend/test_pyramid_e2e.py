"""
金字塔徽章层级端到端测试
验证完整的智能生成流程和配置正确性
"""
import asyncio
import sys
import json
sys.path.insert(0, 'c:\\AI\\genai_chart-1\\backend')

from app.services.generate_service import get_generate_service

async def test_pyramid_badge():
    """测试金字塔徽章层级模板的完整流程"""
    print("=" * 80)
    print("金字塔徽章层级 - 端到端测试")
    print("=" * 80)
    
    # 测试输入文本
    test_cases = [
        {
            "name": "会员荣誉等级",
            "text": "我们公司的荣誉体系分为五个等级，金牌会员占比10%，银牌会员占比15%，铜牌会员占比25%，优秀会员占比30%，普通会员占比20%"
        },
        {
            "name": "需求优先级",
            "text": "产品需求按优先级分为：P0核心功能(5%)、P1重要功能(15%)、P2常规功能(30%)、P3次要功能(35%)、P4低优先级(15%)"
        }
    ]
    
    service = get_generate_service()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"测试用例 {i}: {test_case['name']}")
        print(f"{'='*80}")
        print(f"输入文本: {test_case['text']}")
        
        try:
            # 执行智能生成
            result = await service.generate_smart(user_text=test_case['text'])
            
            # 验证分类
            classification = result['classification']
            print(f"\n✓ 分类结果:")
            print(f"  类型: {classification['type']}")
            print(f"  置信度: {classification['confidence']}")
            print(f"  理由: {classification['reason']}")
            
            # 验证模板选择
            selection = result['selection']
            print(f"\n✓ 模板选择:")
            print(f"  ID: {selection['templateId']}")
            print(f"  名称: {selection['templateName']}")
            print(f"  置信度: {selection['confidence']}")
            print(f"  理由: {selection['reason']}")
            
            # 验证配置
            config = result['config']
            print(f"\n✓ 配置验证:")
            
            # 检查design结构
            if 'design' in config:
                design = config['design']
                structure_type = design.get('structure', {}).get('type')
                items = design.get('items', [])
                
                print(f"  结构类型: {structure_type}")
                print(f"  Items配置: {items}")
                
                # 验证是否符合list-pyramid + badge-card
                assert structure_type == 'list-pyramid', f"结构类型错误: {structure_type}"
                assert len(items) > 0, "Items配置为空"
                assert items[0].get('type') == 'badge-card', f"Item类型错误: {items[0]}"
                
                print(f"  ✓ 结构类型正确: list-pyramid")
                print(f"  ✓ Items类型正确: badge-card")
            else:
                print(f"  ⚠ 警告: 配置中没有design字段")
            
            # 检查data
            if 'data' in config:
                data = config['data']
                print(f"\n✓ 数据结构:")
                print(f"  标题: {data.get('title', 'N/A')}")
                print(f"  描述: {data.get('desc', 'N/A')}")
                
                items = data.get('items', [])
                print(f"  数据项数量: {len(items)}")
                
                # 验证每个数据项
                for idx, item in enumerate(items, 1):
                    label = item.get('label', '')
                    icon = item.get('icon', '')
                    desc = item.get('desc', '')
                    print(f"    {idx}. {label}")
                    print(f"       图标: {icon}")
                    if desc:
                        print(f"       描述: {desc[:50]}...")
                    
                    # 验证icon格式
                    if icon and not icon.startswith('icon:'):
                        print(f"       ⚠ 警告: 图标格式可能不正确: {icon}")
            else:
                print(f"  ⚠ 警告: 配置中没有data字段")
            
            # 输出完整配置（用于调试）
            print(f"\n完整配置:")
            print(json.dumps(config, ensure_ascii=False, indent=2))
            
            # 耗时统计
            timing = result['timing']
            print(f"\n✓ 耗时统计:")
            print(f"  阶段1 (分类): {timing['phase1_classification']}s")
            print(f"  阶段2 (选择): {timing['phase2_selection']}s")
            print(f"  阶段3 (提取): {timing['phase3_extraction']}s")
            print(f"  总计: {timing['total']}s")
            
            print(f"\n✓ 测试用例 {i} 通过！")
            
        except Exception as e:
            print(f"\n✗ 测试失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    print(f"\n{'='*80}")
    print("✓ 所有测试通过！")
    print(f"{'='*80}")
    return True

if __name__ == '__main__':
    success = asyncio.run(test_pyramid_badge())
    sys.exit(0 if success else 1)
