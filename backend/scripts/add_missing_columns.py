"""
添加缺失的数据库字段
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy import text
from app.utils.db import get_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def add_missing_columns():
    """添加缺失的字段到templates表"""
    logger.info("开始添加缺失的数据库字段...")
    
    db = next(get_db())
    try:
        # 添加 structure_type 字段
        logger.info("添加 structure_type 字段...")
        db.execute(text("ALTER TABLE templates ADD COLUMN structure_type VARCHAR(100)"))
        logger.info("✓ structure_type 字段添加成功")
        
        # 添加 keywords 字段
        logger.info("添加 keywords 字段...")
        db.execute(text("ALTER TABLE templates ADD COLUMN keywords TEXT"))
        logger.info("✓ keywords 字段添加成功")
        
        db.commit()
        logger.info("✅ 所有字段添加完成！")
        
    except Exception as e:
        if "duplicate column name" in str(e).lower():
            logger.info("字段已存在，跳过")
        else:
            logger.error(f"添加字段失败: {e}")
            raise
    finally:
        db.close()


if __name__ == "__main__":
    add_missing_columns()
