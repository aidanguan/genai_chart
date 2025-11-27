"""
数据库迁移脚本 - 添加category和structure_type字段
用于支持模板分类体系
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy import text
from app.utils.db import get_db_session, engine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def add_template_category_fields():
    """
    添加category和structure_type字段到templates表
    """
    logger.info("开始数据库迁移：添加category和structure_type字段")
    
    db = get_db_session()
    try:
        # 检查字段是否已存在
        check_columns_sql = text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'templates'
        """)
        
        existing_columns = [row[0] for row in db.execute(check_columns_sql).fetchall()]
        logger.info(f"现有字段: {existing_columns}")
        
        # 添加structure_type字段
        if 'structure_type' not in existing_columns:
            logger.info("添加structure_type字段...")
            db.execute(text("""
                ALTER TABLE templates 
                ADD COLUMN structure_type VARCHAR(100) NULL 
                COMMENT 'AntV structure类型（如list-row、sequence-timeline）'
            """))
            logger.info("✓ structure_type字段添加成功")
        else:
            logger.info("structure_type字段已存在，跳过")
        
        # 添加keywords字段
        if 'keywords' not in existing_columns:
            logger.info("添加keywords字段...")
            db.execute(text("""
                ALTER TABLE templates 
                ADD COLUMN keywords TEXT NULL 
                COMMENT '关键词列表（逗号分隔）'
            """))
            logger.info("✓ keywords字段添加成功")
        else:
            logger.info("keywords字段已存在，跳过")
        
        # 更新category字段的注释
        logger.info("更新category字段注释...")
        db.execute(text("""
            ALTER TABLE templates 
            MODIFY COLUMN category VARCHAR(50) NOT NULL 
            COMMENT '分类(7类之一: chart/comparison/hierarchy/list/quadrant/relationship/sequence)'
        """))
        logger.info("✓ category字段注释更新成功")
        
        # 创建structure_type索引
        try:
            logger.info("创建structure_type索引...")
            db.execute(text("""
                CREATE INDEX idx_structure_type ON templates(structure_type)
            """))
            logger.info("✓ structure_type索引创建成功")
        except Exception as e:
            if 'Duplicate key name' in str(e):
                logger.info("idx_structure_type索引已存在，跳过")
            else:
                raise
        
        db.commit()
        logger.info("数据库迁移完成！")
        
    except Exception as e:
        db.rollback()
        logger.error(f"数据库迁移失败: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    add_template_category_fields()
