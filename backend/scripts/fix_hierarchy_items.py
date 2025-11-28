"""
修复层级对比结构的 items 配置 - 需要两个item类型
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.db import get_db_session
from app.models.template import Template
from sqlalchemy.orm.attributes import flag_modified
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 需要两个item类型的模板配置
HIERARCHY_COMPARE_ITEMS = {
    'compare-hierarchy-left-right': [
        {'type': 'circle-node', 'width': 180},
        {'type': 'plain-text'}
    ],
    'compare-hierarchy-row': [
        {'type': 'letter-card'},
        {'type': 'compact-card'}
    ],
    # relation-circle 系列使用单一 item 即可
    # mindmap-radial 实际上是 relation-circle 类型
}

def fix_hierarchy_items():
    """修复层级对比结构的items配置"""
    db = get_db_session()
    fixed_count = 0
    
    try:
        for template_id, items_config in HIERARCHY_COMPARE_ITEMS.items():
            template = db.query(Template).filter(Template.id == template_id).first()
            
            if not template:
                logger.warning(f"模板 {template_id} 不存在")
                continue
            
            design_config = template.design_config
            if not design_config or 'design' not in design_config:
                logger.warning(f"模板 {template_id} 缺少 design_config")
                continue
            
            # 更新 items 配置为双层结构
            design_config['design']['items'] = items_config
            
            template.design_config = design_config
            flag_modified(template, 'design_config')
            template.updated_at = datetime.utcnow()
            
            logger.info(f"✓ {template_id}: 更新 items 为 {items_config}")
            fixed_count += 1
        
        db.commit()
        logger.info(f"✅ 成功修复 {fixed_count} 个模板")
        
    except Exception as e:
        db.rollback()
        logger.error(f"❌ 修复失败: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    fix_hierarchy_items()
