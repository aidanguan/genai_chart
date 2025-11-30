"""删除并重新创建user_works表"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.db import engine
from app.models.work import UserWork
from sqlalchemy import text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def recreate_user_works_table():
    """删除并重新创建user_works表"""
    try:
        with engine.connect() as conn:
            # 删除旧表
            logger.info("删除旧的user_works表...")
            conn.execute(text("DROP TABLE IF EXISTS user_works"))
            conn.commit()
            logger.info("✓ 旧表已删除")
        
        # 重新创建表
        logger.info("创建新的user_works表...")
        UserWork.__table__.create(engine)
        logger.info("✓ 新表已创建")
        
        # 验证表结构
        from sqlalchemy import inspect
        inspector = inspect(engine)
        columns = inspector.get_columns('user_works')
        logger.info("\n新表结构:")
        for col in columns:
            logger.info(f"  {col['name']}: {col['type']} (nullable={col['nullable']})")
        
        logger.info("\n✅ user_works表重建成功!")
        
    except Exception as e:
        logger.error(f"❌ 重建表失败: {e}")
        raise

if __name__ == "__main__":
    recreate_user_works_table()
