"""
修复数据库中错误的模板结构类型
将 chart-bar-vertical 修正为 chart-column
"""
import sys
import os
import logging

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.db import get_db
from app.models.template import Template

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def fix_template_structure():
    """修复模板结构类型"""
    from sqlalchemy.orm.attributes import flag_modified
    
    with get_db() as db:
        # 查找需要修复的模板
        template = db.query(Template).filter(Template.id == 'bar-chart-vertical').first()
        
        if not template:
            logger.info("未找到需要修复的模板 (bar-chart-vertical)")
            return
        
        logger.info(f"找到模板: {template.name}")
        
        # 检查当前配置
        design_config = template.design_config
        if not design_config or 'design' not in design_config:
            logger.warning("模板配置格式异常")
            return
        
        structure = design_config.get('design', {}).get('structure', {})
        current_type = structure.get('type')
        
        logger.info(f"当前结构类型: {current_type}")
        
        if current_type == 'chart-bar-vertical':
            # 修正结构类型
            design_config['design']['structure']['type'] = 'chart-column'
            # 添加必需的 items 配置
            design_config['design']['items'] = [
                {
                    'type': 'simple',
                    'showIcon': False,
                    'usePaletteColor': True
                }
            ]
            template.design_config = design_config
            # 标记 JSON 字段已修改，否则 SQLAlchemy 不会检测到变化
            flag_modified(template, 'design_config')
            
            # 标记为已修改
            from datetime import datetime
            template.updated_at = datetime.utcnow()
            
            db.commit()
            logger.info("✅ 修复成功: chart-bar-vertical -> chart-column (含 items 配置)")
        elif current_type == 'chart-column':
            # 检查是否有 items 配置
            if 'items' not in design_config.get('design', {}):
                logger.info("⚠️  chart-column 缺少 items 配置，正在添加...")
                design_config['design']['items'] = [
                    {
                        'type': 'simple',
                        'showIcon': False,
                        'usePaletteColor': True
                    }
                ]
                template.design_config = design_config
                # 标记 JSON 字段已修改
                flag_modified(template, 'design_config')
                
                from datetime import datetime
                template.updated_at = datetime.utcnow()
                
                db.commit()
                logger.info("✅ 已添加 items 配置")
            else:
                logger.info("✅ 模板已经是正确的结构类型且包含 items 配置,无需修复")
        else:
            logger.warning(f"⚠️  未知的结构类型: {current_type}")


def main():
    """主函数"""
    try:
        logger.info("开始修复模板结构类型...")
        fix_template_structure()
        logger.info("修复完成!")
    except Exception as e:
        logger.error(f"❌ 修复失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
