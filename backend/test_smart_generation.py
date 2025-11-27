"""
集成测试脚本
测试完整的三阶段智能生成流程
"""
import sys
import os
import asyncio
from pathlib import Path

# 添加项目根目录到路径
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def test_smart_generation():
    """测试智能生成流程"""
    from app.services.generate_service import get_generate_service
    
    logger.info("="*80)
    logger.info("集成测试：智能生成流程")
    logger.info("="*80)
    
    # 测试用例
    test_cases = [
        {
            "name": "顺序型 - 产品开发流程",
            "text": "产品开发流程包括：需求分析、设计、开发、测试、上线五个阶段",
            "expected_type": "sequence"
        },
        {
            "name": "列表型 - 产品功能列表",
            "text": "我们的产品有五大核心功能：智能推荐、数据分析、用户管理、报表生成、权限控制",
            "expected_type": "list"
        },
        {
            "name": "对比型 - 产品对比",
            "text": "产品A的优势：价格便宜、功能丰富。产品B的优势：性能更好、界面更美观",
            "expected_type": "comparison"
        },
        {
            "name": "层级型 - 组织架构",
            "text": "公司组织架构：CEO下设三个部门，技术部门、市场部门、运营部门",
            "expected_type": "hierarchy"
        }
    ]
    
    generate_service = get_generate_service()
    
    for i, test_case in enumerate(test_cases, 1):
        logger.info(f"\n{'='*80}")
        logger.info(f"测试用例 {i}/{len(test_cases)}: {test_case['name']}")
        logger.info(f"{'='*80}")
        logger.info(f"输入文本: {test_case['text']}")
        logger.info(f"期望类型: {test_case['expected_type']}")
        
        try:
            result = await generate_service.generate_smart(test_case['text'])
            
            logger.info(f"\n【阶段1 - 类型识别】")
            logger.info(f"  识别类型: {result['classification']['type']}")
            logger.info(f"  置信度: {result['classification']['confidence']}")
            logger.info(f"  理由: {result['classification']['reason']}")
            
            logger.info(f"\n【阶段2 - 模板选择】")
            logger.info(f"  选中模板: {result['selection']['templateId']}")
            logger.info(f"  模板名称: {result['selection']['templateName']}")
            logger.info(f"  置信度: {result['selection']['confidence']}")
            logger.info(f"  理由: {result['selection']['reason']}")
            
            logger.info(f"\n【阶段3 - 数据提取】")
            logger.info(f"  配置keys: {list(result['config'].keys())}")
            if 'data' in result['config']:
                logger.info(f"  数据项数量: {len(result['config']['data'].get('items', []))}")
            
            logger.info(f"\n【性能统计】")
            logger.info(f"  阶段1耗时: {result['timing']['phase1_classification']}s")
            logger.info(f"  阶段2耗时: {result['timing']['phase2_selection']}s")
            logger.info(f"  阶段3耗时: {result['timing']['phase3_extraction']}s")
            logger.info(f"  总耗时: {result['timing']['total']}s")
            
            # 验证类型是否匹配
            if result['classification']['type'] == test_case['expected_type']:
                logger.info(f"\n✅ 测试通过！类型识别正确")
            else:
                logger.warning(f"\n⚠️ 类型识别不匹配：期望 {test_case['expected_type']}，实际 {result['classification']['type']}")
            
        except Exception as e:
            logger.error(f"\n❌ 测试失败: {e}")
            import traceback
            traceback.print_exc()
    
    logger.info(f"\n{'='*80}")
    logger.info("集成测试完成")
    logger.info(f"{'='*80}")


async def test_type_classification():
    """测试类型识别服务"""
    from app.services.type_classification_service import get_type_classification_service
    
    logger.info("\n单元测试：类型识别服务")
    logger.info("="*80)
    
    service = get_type_classification_service()
    
    test_text = "产品开发流程：需求分析 → 设计 → 开发 → 测试 → 上线"
    result = await service.classify(test_text)
    
    logger.info(f"文本: {test_text}")
    logger.info(f"识别类型: {result['type']}")
    logger.info(f"置信度: {result['confidence']}")
    logger.info(f"理由: {result['reason']}")


async def test_template_selection():
    """测试模板选择服务"""
    from app.services.template_selection_service import get_template_selection_service
    
    logger.info("\n单元测试：模板选择服务")
    logger.info("="*80)
    
    service = get_template_selection_service()
    
    test_text = "产品开发流程：需求分析 → 设计 → 开发 → 测试 → 上线"
    content_type = "sequence"
    
    result = await service.select(test_text, content_type)
    
    logger.info(f"文本: {test_text}")
    logger.info(f"内容类型: {content_type}")
    logger.info(f"选中模板: {result['templateId']}")
    logger.info(f"模板名称: {result['templateName']}")
    logger.info(f"置信度: {result['confidence']}")
    logger.info(f"理由: {result['reason']}")


async def main():
    """主函数"""
    logger.info("开始运行集成测试...")
    
    # 测试各个服务
    await test_type_classification()
    await test_template_selection()
    
    # 测试完整流程
    await test_smart_generation()
    
    logger.info("\n✓ 所有测试完成！")


if __name__ == "__main__":
    asyncio.run(main())
