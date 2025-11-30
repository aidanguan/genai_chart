"""
修复柱状图模板的data_schema
将 data.data 改为 data.items (符合AntV Infographic ChartColumn组件的要求)
"""
import sys
import os
import logging

# 添加backend目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.db import get_db_session
from app.models.template import Template
from sqlalchemy.orm.attributes import flag_modified

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def fix_chart_column_templates():
    """修复柱状图模板的data_schema"""
    db = get_db_session()
    
    try:
        # 需要修复的模板ID列表
        template_ids = ['bar-chart-vertical', 'chart-column-colorful']
        
        for template_id in template_ids:
            logger.info(f"\n{'='*60}")
            logger.info(f"处理模板: {template_id}")
            logger.info(f"{'='*60}")
            
            # 获取模板
            template = db.query(Template).filter(Template.id == template_id).first()
            
            if not template:
                logger.warning(f"⚠️  模板不存在: {template_id}")
                continue
            
            # 检查当前schema
            import json
            logger.info(f"\n当前data_schema:")
            logger.info(json.dumps(template.data_schema, indent=2, ensure_ascii=False))
            
            # 修复schema: data.data -> data.items
            if template.data_schema and 'dataFields' in template.data_schema:
                if 'data' in template.data_schema['dataFields']:
                    # 将 'data' 字段重命名为 'items'
                    old_data_field = template.data_schema['dataFields']['data']
                    template.data_schema['dataFields']['items'] = old_data_field
                    del template.data_schema['dataFields']['data']
                    
                    # 标记为已修改
                    flag_modified(template, 'data_schema')
                    
                    logger.info(f"\n✅ 已修复: data.data -> data.items")
                    logger.info(f"\n修复后data_schema:")
                    logger.info(json.dumps(template.data_schema, indent=2, ensure_ascii=False))
                else:
                    logger.info(f"✓ 已经是正确的结构 (使用items字段)")
            else:
                logger.warning(f"⚠️  data_schema结构异常")
        
        # 提交更改
        db.commit()
        logger.info(f"\n{'='*60}")
        logger.info("✅ 所有修复已提交到数据库")
        logger.info(f"{'='*60}")
        
    except Exception as e:
        db.rollback()
        logger.error(f"❌ 修复失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    fix_chart_column_templates()
