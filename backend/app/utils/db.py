"""
数据库连接和初始化工具
"""
import logging
from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from app.config import get_settings

logger = logging.getLogger(__name__)

# 获取配置
settings = get_settings()

# 创建数据库引擎
# 开发环境使用SQLite,生产环境可切换到PostgreSQL
DATABASE_URL = getattr(settings, 'DATABASE_URL', 'sqlite:///./infographic.db')

# SQLite特殊配置
if DATABASE_URL.startswith('sqlite'):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=settings.DEBUG_MODE
    )
else:
    engine = create_engine(
        DATABASE_URL,
        echo=settings.DEBUG_MODE,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20
    )

# 创建Session工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """初始化数据库,创建所有表"""
    from app.models.base import Base
    # 导入所有模型确保被注册
    from app.models.template import Template
    from app.models.work import UserWork
    
    try:
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        logger.info("数据库表创建成功")
    except Exception as e:
        logger.error(f"数据库表创建失败: {e}")
        raise


@contextmanager
def get_db() -> Generator[Session, None, None]:
    """
    获取数据库会话的上下文管理器
    
    用法:
        with get_db() as db:
            # 使用db进行数据库操作
            pass
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_db_session() -> Session:
    """
    获取数据库会话(用于依赖注入)
    
    用法:
        db = get_db_session()
        try:
            # 数据库操作
            db.commit()
        except:
            db.rollback()
        finally:
            db.close()
    """
    return SessionLocal()
