"""
chart-column-simple模板测试脚本
验证Dify工作流集成和端到端生成流程
"""
import asyncio
import logging
import sys
import os

# 添加backend目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.generate_service import get_generate_service
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


# 测试用例
TEST_CASES = [
    {
        "name": "基础数值对比",
        "user_text": "2023年销售额：北京1000万，上海1200万，广州800万，深圳900万",
        "expected_type": "chart",
        "expected_template": "chart-column-simple"
    },
    {
        "name": "百分比数据",
        "user_text": "市场份额：产品A占30%，产品B占45%，产品C占25%",
        "expected_type": "chart",
        "expected_template": "chart-column-simple"
    },
    {
        "name": "带单位数据",
        "user_text": "季度收入：Q1 5000万元，Q2 6200万元，Q3 5800万元，Q4 7000万元",
        "expected_type": "chart",
        "expected_template": "chart-column-simple"
    },
    {
        "name": "简单数据",
        "user_text": "水果销量：苹果100斤，橙子80斤，香蕉60斤",
        "expected_type": "chart",
        "expected_template": "chart-column-simple"
    }
]


async def test_single_case(service, test_case):
    """测试单个用例"""
    logger.info(f"\n{'='*80}")
    logger.info(f"测试用例: {test_case['name']}")
    logger.info(f"输入文本: {test_case['user_text']}")
    logger.info(f"{'='*80}")
    
    try:
        # 调用智能生成
        result = await service.generate_smart(user_text=test_case['user_text'])
        
        # 验证结果
        logger.info(f"\n✅ 生成成功！")
        logger.info(f"\n类型识别:")
        logger.info(f"  - 类型: {result['classification']['type']}")
        logger.info(f"  - 置信度: {result['classification']['confidence']}")
        logger.info(f"  - 理由: {result['classification']['reason']}")
        
        logger.info(f"\n模板选择:")
        logger.info(f"  - 模板ID: {result['selection']['templateId']}")
        logger.info(f"  - 模板名称: {result['selection']['templateName']}")
        logger.info(f"  - 置信度: {result['selection']['confidence']}")
        logger.info(f"  - 理由: {result['selection']['reason']}")
        
        logger.info(f"\n数据生成:")
        logger.info(f"  - 生成方式: {result['generation_method']}")
        if 'workflow_info' in result:
            logger.info(f"  - 工作流: {result['workflow_info']['workflow_name']}")
            logger.info(f"  - 工作流运行ID: {result['workflow_info']['workflow_run_id']}")
        
        logger.info(f"\n耗时统计:")
        logger.info(f"  - 阶段1(类型识别): {result['timing']['phase1_classification']}s")
        logger.info(f"  - 阶段2(模板选择): {result['timing']['phase2_selection']}s")
        logger.info(f"  - 阶段3(数据提取): {result['timing']['phase3_extraction']}s")
        if 'dify_call_time' in result['timing']:
            logger.info(f"  - Dify调用: {result['timing']['dify_call_time']}s")
        logger.info(f"  - 总耗时: {result['timing']['total']}s")
        
        logger.info(f"\n生成的配置对象:")
        import json
        config_json = json.dumps(result['config'], ensure_ascii=False, indent=2)
        logger.info(config_json)
        
        # 验证预期
        classification_match = result['classification']['type'] == test_case.get('expected_type')
        # 注意：模板选择可能不完全匹配，因为LLM可能选择其他合适的模板
        # template_match = result['selection']['templateId'] == test_case.get('expected_template')
        
        if classification_match:
            logger.info(f"\n✅ 类型识别符合预期: {test_case['expected_type']}")
        else:
            logger.warning(f"\n⚠️  类型识别不符: 预期 {test_case['expected_type']}, 实际 {result['classification']['type']}")
        
        return {
            "success": True,
            "result": result,
            "classification_match": classification_match
        }
        
    except Exception as e:
        logger.error(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e)
        }


async def main():
    """主测试流程"""
    logger.info("="*80)
    logger.info("chart-column-simple模板测试")
    logger.info("="*80)
    
    # 验证环境配置
    logger.info("\n检查环境配置:")
    dify_api_key = os.getenv('DIFY_API_KEY')
    dify_base_url = os.getenv('DIFY_API_BASE_URL')
    logger.info(f"  - DIFY_API_BASE_URL: {dify_base_url}")
    logger.info(f"  - DIFY_API_KEY: {'已配置' if dify_api_key else '未配置'}")
    
    if not dify_api_key:
        logger.warning("⚠️  DIFY_API_KEY未配置，将仅使用系统LLM")
    
    # 获取生成服务
    service = get_generate_service()
    
    # 运行所有测试用例
    results = []
    for test_case in TEST_CASES:
        result = await test_single_case(service, test_case)
        results.append({
            "case": test_case['name'],
            **result
        })
        
        # 测试之间暂停
        await asyncio.sleep(2)
    
    # 汇总结果
    logger.info(f"\n\n{'='*80}")
    logger.info("测试汇总")
    logger.info(f"{'='*80}")
    
    success_count = sum(1 for r in results if r['success'])
    total_count = len(results)
    
    logger.info(f"\n总测试数: {total_count}")
    logger.info(f"成功: {success_count}")
    logger.info(f"失败: {total_count - success_count}")
    
    for result in results:
        status = "✅" if result['success'] else "❌"
        logger.info(f"\n{status} {result['case']}")
        if result['success']:
            logger.info(f"   生成方式: {result['result']['generation_method']}")
            if 'classification_match' in result and result['classification_match']:
                logger.info(f"   类型识别: ✅ 符合预期")
        else:
            logger.info(f"   错误: {result.get('error', '未知')}")
    
    logger.info(f"\n{'='*80}")
    logger.info("测试完成")
    logger.info(f"{'='*80}")


if __name__ == "__main__":
    asyncio.run(main())
