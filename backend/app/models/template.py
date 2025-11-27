"""
模板数据库模型
"""
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, JSON, Index
from app.models.base import Base


class Template(Base):
    """模板表"""
    __tablename__ = "templates"
    
    # 字段定义
    id = Column(String(100), primary_key=True, comment="模板唯一标识")
    name = Column(String(200), nullable=False, comment="模板名称(中文)")
    category = Column(String(50), nullable=False, index=True, comment="分类(7类之一: chart/comparison/hierarchy/list/quadrant/relationship/sequence)")
    structure_type = Column(String(100), nullable=True, index=True, comment="AntV structure类型（如list-row、sequence-timeline）")
    description = Column(Text, nullable=True, comment="模板描述")
    keywords = Column(Text, nullable=True, comment="关键词列表（逗号分隔）")
    use_cases = Column(Text, nullable=True, comment="适用场景说明")
    preview_url = Column(String(500), nullable=True, comment="预览图URL")
    data_schema = Column(JSON, nullable=False, comment="数据结构Schema")
    design_config = Column(JSON, nullable=False, comment="AntV设计配置")
    tags = Column(JSON, nullable=True, comment="标签数组")
    sort_order = Column(Integer, default=0, comment="排序权重")
    is_active = Column(Boolean, default=True, comment="是否启用")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    # 复合索引
    __table_args__ = (
        Index('idx_category_sort', 'category', 'sort_order'),
    )
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "structureType": self.structure_type,
            "description": self.description,
            "keywords": self.keywords.split(',') if self.keywords else [],
            "useCases": self.use_cases,
            "previewUrl": self.preview_url,
            "dataSchema": self.data_schema,
            "designConfig": self.design_config,
            "tags": self.tags,
            "sortOrder": self.sort_order,
            "isActive": self.is_active,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None
        }
