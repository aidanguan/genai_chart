"""
修复使用无效结构类型的模板
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.db import get_db_session
from app.models.template import Template
from sqlalchemy.orm.attributes import flag_modified
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 无效结构类型到有效类型的映射
STRUCTURE_TYPE_MAPPING = {
    'quadrant-swot': 'quadrant',
    'tree-org': 'hierarchy-tree',
    'comparison-column': 'compare-binary-horizontal',
    'mindmap-radial': 'relation-circle',
    'timeline-horizontal': 'sequence-timeline',
    'list-checklist': 'list-column',
}

# 每种结构类型需要的 items 配置
STRUCTURE_ITEMS_CONFIG = {
    'quadrant': [{'type': 'quarter-simple-card'}],
    'hierarchy-tree': [{'type': 'rounded-rect-node'}],
    'compare-binary-horizontal': [{'type': 'simple', 'iconType': 'circle', 'iconSize': 40}],
    'relation-circle': [{'type': 'simple'}],
    'sequence-timeline': [{'type': 'simple', 'showIcon': False}],
    'list-column': [{'type': 'done-list'}],
}

# 特殊的 item 类型映射
SPECIAL_ITEM_MAPPING = {
    'priority-card': 'quarter-simple-card',  # quadrant-priority-matrix
}


def fix_invalid_structures():
    """修复所有使用无效结构类型的模板"""
    db = get_db_session()
    fixed_count = 0
    
    try:
        # 获取所有模板
        templates = db.query(Template).all()
        logger.info(f"找到 {len(templates)} 个模板")
        
        for template in templates:
            try:
                modified = False
                design_config = template.design_config
                
                if not design_config or 'design' not in design_config:
                    continue
                
                design = design_config['design']
                
                # 检查并修复结构类型
                if 'structure' in design and isinstance(design['structure'], dict):
                    structure_type = design['structure'].get('type')
                    
                    # 修复无效的结构类型
                    if structure_type in STRUCTURE_TYPE_MAPPING:
                        new_type = STRUCTURE_TYPE_MAPPING[structure_type]
                        design['structure']['type'] = new_type
                        logger.info(f"{template.id}: 结构类型 {structure_type} -> {new_type}")
                        modified = True
                        structure_type = new_type  # 更新变量以便后续使用
                    
                    # 确保有 items 配置
                    if 'items' not in design or not design['items']:
                        if structure_type in STRUCTURE_ITEMS_CONFIG:
                            design['items'] = STRUCTURE_ITEMS_CONFIG[structure_type]
                            logger.info(f"✓ {template.id}: 添加默认 items 配置 {design['items']}")
                            modified = True
                    else:
                        # 检查并修复 items 中的无效类型
                        items_modified = False
                        for i, item in enumerate(design['items']):
                            if isinstance(item, dict) and 'type' in item:
                                if item['type'] in SPECIAL_ITEM_MAPPING:
                                    new_item_type = SPECIAL_ITEM_MAPPING[item['type']]
                                    design['items'][i]['type'] = new_item_type
                                    logger.info(f"✓ {template.id}: items[{i}].type {item['type']} -> {new_item_type}")
                                    items_modified = True
                        
                        if items_modified:
                            modified = True
                
                # 保存修改
                if modified:
                    template.design_config = design_config
                    flag_modified(template, 'design_config')
                    template.updated_at = datetime.utcnow()
                    fixed_count += 1
                    
            except Exception as e:
                logger.error(f"处理模板 {template.id} 时出错: {e}")
                continue
        
        # 提交所有更改
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


def main():
    """主函数"""
    try:
        logger.info("开始修复无效的结构类型...")
        fix_invalid_structures()
        logger.info("修复完成!")
    except Exception as e:
        logger.error(f"❌ 执行失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
