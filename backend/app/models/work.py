"""
用户作品数据库模型
"""
from datetime import datetime
from sqlalchemy import Column, String, Text, BigInteger, DateTime, JSON, ForeignKey, Index
from app.models.base import Base


class UserWork(Base):
    """用户作品表"""
    __tablename__ = "user_works"
    
    # 字段定义
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="作品ID")
    user_id = Column(String(100), index=True, nullable=True, comment="用户标识")
    title = Column(String(200), nullable=True, comment="作品标题")
    template_id = Column(String(100), ForeignKey('templates.id'), nullable=False, comment="使用的模板ID")
    input_text = Column(Text, nullable=False, comment="用户输入的原始文本")
    infographic_config = Column(JSON, nullable=False, comment="完整的Infographic配置")
    thumbnail_url = Column(String(500), nullable=True, comment="缩略图URL")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "userId": self.user_id,
            "title": self.title,
            "templateId": self.template_id,
            "inputText": self.input_text,
            "infographicConfig": self.infographic_config,
            "thumbnailUrl": self.thumbnail_url,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None
        }
