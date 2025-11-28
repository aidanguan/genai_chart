"""
修复模板中使用不存在的 item 类型的问题
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

# 错误 item 类型到正确类型的映射
ITEM_TYPE_MAPPING = {
    # sequence-circular-icon: icon -> simple (带图标)
    'icon': 'simple',
    
    # sequence-timeline-milestone: milestone-card -> indexed-card
    'milestone-card': 'indexed-card',
    
    # compare-binary-vs-card: vs-card -> compact-card
    'vs-card': 'compact-card',
    
    # list-sector-numbered: numbered-badge -> indexed-card
    'numbered-badge': 'indexed-card',
    
    # list-pyramid-badge: badge -> badge-card
    'badge': 'badge-card',
    
    # relation-circle-connected: connected-card -> simple
    'connected-card': 'simple',
    
    # sequence-circular-icon: icon-card -> badge-card
    'icon-card': 'badge-card',
}

# 需要将 item 字段转换为 items 数组的模板
TEMPLATES_NEED_ITEMS_ARRAY = [
    'sequence-circular-icon',
    'sequence-timeline-milestone',
    'list-pyramid-badge',
    'list-sector-numbered',
    'compare-binary-vs-card',
    'relation-circle-connected',
    'timeline-horizontal',
    'checklist',
    'list-grid-icon-card',
    'list-column-icon-card',
    'compare-hierarchy-left-right',
    'compare-hierarchy-row',
]


def fix_invalid_item_types():
    """修复所有使用无效 item 类型的模板"""
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
                    logger.warning(f"跳过 {template.id}: 缺少 design 配置")
                    continue
                
                design = design_config['design']
                
                # 情况1: 使用了 item 字段 (旧格式)，需要转换为 items 数组
                if 'item' in design:
                    old_item = design['item']
                    
                    # 如果是无效类型，先映射到有效类型
                    if old_item in ITEM_TYPE_MAPPING:
                        new_item = ITEM_TYPE_MAPPING[old_item]
                        logger.info(f"{template.id}: 映射 item 类型: {old_item} -> {new_item}")
                    else:
                        new_item = old_item
                    
                    # 转换为 items 数组格式
                    design['items'] = [{'type': new_item}]
                    
                    # 特殊配置处理
                    if template.id == 'sequence-circular-icon' and new_item == 'simple':
                        # 为 simple 添加图标显示配置
                        design['items'][0].update({
                            'iconType': 'circle',
                            'iconSize': 36
                        })
                    elif template.id in ['compare-binary-vs-card', 'list-grid-icon-card', 'list-column-icon-card']:
                        # 为卡片类型添加适当的尺寸
                        design['items'][0].update({
                            'width': 200,
                            'height': 80
                        })
                    
                    # 删除旧的 item 字段
                    del design['item']
                    
                    logger.info(f"✓ {template.id}: item -> items[{new_item}]")
                    modified = True
                
                # 情况2: 已经使用 items 数组，但类型无效
                elif 'items' in design and isinstance(design['items'], list):
                    for i, item_config in enumerate(design['items']):
                        if isinstance(item_config, dict) and 'type' in item_config:
                            old_type = item_config['type']
                            if old_type in ITEM_TYPE_MAPPING:
                                new_type = ITEM_TYPE_MAPPING[old_type]
                                design['items'][i]['type'] = new_type
                                logger.info(f"✓ {template.id}: items[{i}].type: {old_type} -> {new_type}")
                                modified = True
                
                # 情况3: 缺少 item/items 配置
                elif 'items' not in design and template.id in TEMPLATES_NEED_ITEMS_ARRAY:
                    # 根据模板ID推断合适的 item 类型
                    if 'icon' in template.id or 'timeline' in template.id:
                        item_type = 'simple'
                        design['items'] = [{'type': item_type, 'iconType': 'circle', 'iconSize': 32}]
                    elif 'checklist' in template.id:
                        item_type = 'done-list'
                        design['items'] = [{'type': item_type}]
                    elif 'card' in template.id:
                        item_type = 'compact-card'
                        design['items'] = [{'type': item_type}]
                    else:
                        item_type = 'simple'
                        design['items'] = [{'type': item_type}]
                    
                    logger.info(f"✓ {template.id}: 添加缺失的 items 配置 [{item_type}]")
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
        logger.info("开始修复无效的 item 类型...")
        fix_invalid_item_types()
        logger.info("修复完成!")
    except Exception as e:
        logger.error(f"❌ 执行失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
