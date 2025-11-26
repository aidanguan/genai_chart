"""
作品Repository
"""
import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.work import UserWork

logger = logging.getLogger(__name__)


class WorkRepository:
    """作品数据访问类"""
    
    def __init__(self, db: Session):
        """
        初始化Repository
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def create(self, work: UserWork) -> UserWork:
        """
        创建作品
        
        Args:
            work: 作品对象
        
        Returns:
            创建的作品
        """
        self.db.add(work)
        self.db.commit()
        self.db.refresh(work)
        return work
    
    def get_by_id(self, work_id: int) -> Optional[UserWork]:
        """
        根据ID获取作品
        
        Args:
            work_id: 作品ID
        
        Returns:
            作品对象或None
        """
        return self.db.query(UserWork).filter(UserWork.id == work_id).first()
    
    def get_all(
        self,
        user_id: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> tuple[List[UserWork], int]:
        """
        获取作品列表(分页)
        
        Args:
            user_id: 用户ID筛选(可选)
            page: 页码(从1开始)
            page_size: 每页数量
        
        Returns:
            (作品列表, 总数)
        """
        query = self.db.query(UserWork)
        
        if user_id:
            query = query.filter(UserWork.user_id == user_id)
        
        # 总数
        total = query.count()
        
        # 排序和分页
        works = query.order_by(
            UserWork.created_at.desc()
        ).offset((page - 1) * page_size).limit(page_size).all()
        
        return works, total
