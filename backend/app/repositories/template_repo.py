"""
模板Repository
"""
import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from app.models.template import Template

logger = logging.getLogger(__name__)


class TemplateRepository:
    """模板数据访问类"""
    
    def __init__(self, db: Session):
        """
        初始化Repository
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def get_all(
        self,
        category: Optional[str] = None,
        keyword: Optional[str] = None,
        is_active: bool = True,
        page: int = 1,
        page_size: int = 20
    ) -> tuple[List[Template], int]:
        """
        获取模板列表(分页)
        
        Args:
            category: 分类筛选
            keyword: 搜索关键词
            is_active: 是否只返回激活的模板
            page: 页码(从1开始)
            page_size: 每页数量
        
        Returns:
            (模板列表, 总数)
        """
        query = self.db.query(Template)
        
        # 筛选条件
        if is_active:
            query = query.filter(Template.is_active == True)
        
        if category:
            query = query.filter(Template.category == category)
        
        if keyword:
            # 搜索名称、描述、适用场景
            search_filter = or_(
                Template.name.contains(keyword),
                Template.description.contains(keyword),
                Template.use_cases.contains(keyword)
            )
            query = query.filter(search_filter)
        
        # 总数
        total = query.count()
        
        # 排序和分页
        templates = query.order_by(
            Template.sort_order.desc(),
            Template.created_at.desc()
        ).offset((page - 1) * page_size).limit(page_size).all()
        
        return templates, total
    
    def get_by_id(self, template_id: str) -> Optional[Template]:
        """
        根据ID获取模板
        
        Args:
            template_id: 模板ID
        
        Returns:
            模板对象或None
        """
        return self.db.query(Template).filter(
            Template.id == template_id,
            Template.is_active == True
        ).first()
    
    def get_by_category(self, category: str) -> List[Template]:
        """
        根据分类获取模板
        
        Args:
            category: 分类
        
        Returns:
            模板列表
        """
        return self.db.query(Template).filter(
            Template.category == category,
            Template.is_active == True
        ).order_by(Template.sort_order.desc()).all()
    
    def get_categories(self) -> List[Dict[str, Any]]:
        """
        获取所有分类及统计
        
        Returns:
            分类列表,包含名称和数量
        """
        # 定义7大分类
        categories = {
            "chart": {"name": "图表型", "description": "数值展示,柱状图等可视化图表"},
            "comparison": {"name": "对比型", "description": "优劣对比、SWOT分析"},
            "hierarchy": {"name": "层级型", "description": "组织结构、分类信息"},
            "list": {"name": "列表型", "description": "步骤说明、清单、简单信息罗列"},
            "quadrant": {"name": "四象限型", "description": "市场定位、风险评估"},
            "relation": {"name": "关系型", "description": "关系网络、关联分析"},
            "sequence": {"name": "顺序型", "description": "时间线、流程图、递进关系"}
        }
        
        # 统计每个分类的模板数量
        result = self.db.query(
            Template.category,
            func.count(Template.id).label('count')
        ).filter(
            Template.is_active == True
        ).group_by(Template.category).all()
        
        # 构建返回结果
        category_list = []
        count_map = {item.category: item.count for item in result}
        
        for code, info in categories.items():
            category_list.append({
                "code": code,
                "name": info["name"],
                "description": info["description"],
                "count": count_map.get(code, 0)
            })
        
        return category_list
