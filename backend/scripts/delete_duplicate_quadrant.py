"""
删除重复的四象限模板 quadrant-priority-matrix
保留 matrix-2x2
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.db import get_db_session
from app.models.template import Template
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def delete_duplicate_template():
    """删除重复的 quadrant-priority-matrix 模板"""
    db = get_db_session()
    
    try:
        # 查找要删除的模板
        template = db.query(Template).filter(Template.id == 'quadrant-priority-matrix').first()
        
        if not template:
            logger.info("模板 quadrant-priority-matrix 不存在,无需删除")
            return
        
        logger.info(f"找到模板: {template.name} (ID: {template.id})")
        logger.info(f"  分类: {template.category}")
        logger.info(f"  描述: {template.description}")
        
        # 删除模板
        db.delete(template)
        db.commit()
        
        logger.info("✅ 成功删除模板 quadrant-priority-matrix")
        
        # 验证删除
        verify = db.query(Template).filter(Template.id == 'quadrant-priority-matrix').first()
        if verify is None:
            logger.info("✓ 验证: 模板已从数据库中删除")
        else:
            logger.error("✗ 验证失败: 模板仍然存在")
        
        # 确认 matrix-2x2 仍然存在
        matrix_2x2 = db.query(Template).filter(Template.id == 'matrix-2x2').first()
        if matrix_2x2:
            logger.info(f"✓ 确认: matrix-2x2 模板仍然存在 ({matrix_2x2.name})")
        else:
            logger.warning("⚠ 警告: matrix-2x2 模板不存在")
        
    except Exception as e:
        db.rollback()
        logger.error(f"❌ 删除失败: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    logger.info("开始删除重复的四象限模板...")
    delete_duplicate_template()
    logger.info("完成!")
