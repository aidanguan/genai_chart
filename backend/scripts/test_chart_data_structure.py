"""
测试柱状图生成并检查实际数据结构
"""
import asyncio
import logging
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.generate_service import get_generate_service
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def test_chart_generation():
    """测试柱状图生成"""
    logger.info("="*80)
    logger.info("柱状图生成测试")
    logger.info("="*80)
    
    service = get_generate_service()
    
    # 测试文本
    test_text = "2023年销售额：北京1000万，上海1200万，广州800万，深圳900万"
    
    logger.info(f"\n输入文本: {test_text}")
    
    try:
        # 调用智能生成
        result = await service.generate_smart(user_text=test_text)
        
        logger.info(f"\n✅ 生成成功！")
        logger.info(f"\n模板ID: {result['selection']['templateId']}")
        logger.info(f"模板名称: {result['selection']['templateName']}")
        
        # 打印完整的config
        logger.info(f"\n{'='*80}")
        logger.info("生成的完整配置:")
        logger.info(f"{'='*80}")
        config_json = json.dumps(result['config'], ensure_ascii=False, indent=2)
        logger.info(config_json)
        
        # 重点检查data结构
        logger.info(f"\n{'='*80}")
        logger.info("数据结构检查:")
        logger.info(f"{'='*80}")
        
        config_data = result['config'].get('data', {})
        logger.info(f"\n顶层data键: {list(config_data.keys())}")
        
        if 'items' in config_data:
            logger.info(f"✅ 包含items字段")
            logger.info(f"items数量: {len(config_data['items'])}")
            logger.info(f"items内容: {json.dumps(config_data['items'], ensure_ascii=False, indent=2)}")
        else:
            logger.warning(f"⚠️  缺少items字段")
        
        if 'data' in config_data:
            logger.warning(f"⚠️  包含错误的data字段 (应该是items)")
            logger.info(f"data内容: {json.dumps(config_data['data'], ensure_ascii=False, indent=2)}")
        
        # 检查design配置
        logger.info(f"\n{'='*80}")
        logger.info("Design配置检查:")
        logger.info(f"{'='*80}")
        design = result['config'].get('design', {})
        logger.info(f"structure.type: {design.get('structure', {}).get('type')}")
        logger.info(f"items配置: {json.dumps(design.get('items', []), ensure_ascii=False, indent=2)}")
        
        return result
        
    except Exception as e:
        logger.error(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    asyncio.run(test_chart_generation())
