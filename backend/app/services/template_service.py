"""
模板服务
管理AntV Infographic模板信息
"""
import logging
from typing import List, Dict, Any, Optional
from app.utils.prompts import TEMPLATE_SCHEMAS

logger = logging.getLogger(__name__)


# AntV Infographic 模板配置映射
TEMPLATE_DESIGN_MAP = {
    "list-row-simple-horizontal-arrow": {
        "template": "list-row-horizontal-icon-arrow"
    },
    "list-row-horizontal-icon-arrow": {
        "template": "list-row-horizontal-icon-arrow"
    },
    "list-column-simple-vertical": {
        "design": {
            "structure": {"type": "list-column"},
            "title": "default",
            "item": "simple"
        }
    },
    "list-column-simple": {
        "design": {
            "structure": {"type": "list-column"},
            "title": "default",
            "item": "simple"
        }
    },
    "checklist": {
        "design": {
            "structure": {"type": "list-column"},
            "title": "default",
            "item": "badge-card"  # 使用badge-card样式展示检查项
        }
    },
    "timeline-horizontal": {
        "design": {
            "structure": {"type": "timeline-horizontal"},
            "title": "default"
        }
    },
    "pyramid-layer": {
        "design": {
            "structure": {"type": "list-pyramid"},
            "title": "default",
            "items": [{"type": "badge-card"}]
        }
    },
    "mindmap-radial": {
        "design": {
            "structure": {"type": "mindmap-radial"},
            "title": "default"
        }
    },
    "matrix-2x2": {
        "design": {
            "structure": {"type": "quadrant"},
            "title": "default",
            "items": [{"type": "quarter-simple-card"}]  # 使用quarter-simple-card样式展示四象限
        }
    },
    "timeline-horizontal": {
        "design": {
            "structure": {"type": "timeline-horizontal"},
            "title": "default",
            "item": "badge-card"  # 时间线需要item配置
        }
    },
    "comparison-two-column": {
        "design": {
            "structure": {"type": "comparison-column"},
            "title": "default",
            "item": "simple"  # 对比列表使用simple样式
        }
    },
    "swot-analysis": {
        "template": "compare-swot"  # 使用AntV Infographic内置的compare-swot模板
    },
    "org-tree": {
        "design": {
            "structure": {"type": "hierarchy-tree"},
            "title": "default",
            "item": "badge-card"  # 组织树使用badge-card
        }
    },
    "compare-hierarchy-left-right": {
        "template": "compare-hierarchy-left-right-circle-node-pill-badge"
    },
    "compare-hierarchy-left-right-circle-node-pill-badge": {
        "template": "compare-hierarchy-left-right-circle-node-pill-badge"
    },
    "compare-binary-horizontal": {
        "design": {
            "structure": {
                "type": "compare-binary-horizontal",
                "dividerType": "vs"
            },
            "title": "default",
            "items": [{"type": "simple", "iconType": "circle", "iconSize": 40}]
        }
    },
    "compare-binary-vs": {
        "design": {
            "structure": {
                "type": "compare-binary-horizontal",
                "dividerType": "vs"
            },
            "title": "default",
            "items": [{"type": "badge-card"}]
        }
    },
}

# 模板元数据（基于AntV Infographic内置模板）
TEMPLATE_METADATA = [
    {
        "id": "list-row-simple-horizontal-arrow",
        "name": "简单横向流程图",
        "category": "流程图",
        "description": "带箭头的横向列表布局，适合展示线性流程",
        "适用场景": "步骤说明、流程展示、操作指南",
        "dataSchema": TEMPLATE_SCHEMAS.get("list-row-simple-horizontal-arrow", {})
    },
    {
        "id": "list-row-horizontal-icon-arrow",
        "name": "图标横向流程图",
        "category": "流程图",
        "description": "带图标和箭头的横向流程图，视觉效果更丰富",
        "适用场景": "产品流程、服务流程、工作流程",
        "dataSchema": TEMPLATE_SCHEMAS.get("list-row-horizontal-icon-arrow", {})
    },
    {
        "id": "list-column-simple-vertical",
        "name": "简单纵向列表",
        "category": "列表图",
        "description": "纵向列表布局，适合展示层级关系",
        "适用场景": "排名展示、要点罗列、层级说明",
        "dataSchema": {
            "description": "纵向列表",
            "dataFields": {
                "title": {"type": "string", "required": False},
                "items": {
                    "type": "array",
                    "required": True,
                    "itemSchema": {
                        "label": {"type": "string", "required": True},
                        "desc": {"type": "string", "required": False}
                    }
                }
            }
        }
    },
    {
        "id": "pyramid-layer",
        "name": "金字塔层级图",
        "category": "层级图",
        "description": "金字塔型布局，展示层级结构",
        "适用场景": "优先级展示、层级结构、组织架构",
        "dataSchema": {
            "description": "金字塔图",
            "dataFields": {
                "title": {"type": "string", "required": False},
                "items": {
                    "type": "array",
                    "required": True,
                    "itemSchema": {
                        "label": {"type": "string", "required": True},
                        "desc": {"type": "string", "required": False}
                    }
                }
            }
        }
    }
]


class TemplateService:
    """模板服务类(重构为从数据库读取)"""
    
    def __init__(self):
        """初始化模板服务"""
        from app.utils.db import get_db_session
        from app.repositories.template_repo import TemplateRepository
        self._get_db = get_db_session
        self._repo_class = TemplateRepository
    
    def get_all_templates(
        self,
        category: Optional[str] = None,
        keyword: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """
        获取所有模板(分页)
        
        Args:
            category: 分类筛选
            keyword: 搜索关键词
            page: 页码
            page_size: 每页数量
        
        Returns:
            Dict: 包含模板列表和分页信息
        """
        db = self._get_db()
        try:
            repo = self._repo_class(db)
            templates, total = repo.get_all(category, keyword, True, page, page_size)
            return {
                "templates": [t.to_dict() for t in templates],
                "total": total,
                "page": page,
                "pageSize": page_size
            }
        finally:
            db.close()
    
    def get_template_by_id(self, template_id: str) -> Optional[Dict[str, Any]]:
        """
        根据ID获取模板
        
        Args:
            template_id: 模板ID
        
        Returns:
            Optional[Dict]: 模板信息，未找到时返回None
        """
        db = self._get_db()
        try:
            repo = self._repo_class(db)
            template = repo.get_by_id(template_id)
            return template.to_dict() if template else None
        finally:
            db.close()
    
    def get_templates_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        根据分类获取模板
        
        Args:
            category: 分类代码
        
        Returns:
            List[Dict]: 模板列表
        """
        db = self._get_db()
        try:
            repo = self._repo_class(db)
            templates = repo.get_by_category(category)
            return [t.to_dict() for t in templates]
        finally:
            db.close()
    
    def get_categories(self) -> List[Dict[str, Any]]:
        """
        获取所有分类及统计
        
        Returns:
            List[Dict]: 分类列表
        """
        db = self._get_db()
        try:
            repo = self._repo_class(db)
            return repo.get_categories()
        finally:
            db.close()
    
    def search_templates(self, keyword: str) -> List[Dict[str, Any]]:
        """
        搜索模板
        
        Args:
            keyword: 搜索关键词
        
        Returns:
            List[Dict]: 匹配的模板列表
        """
        db = self._get_db()
        try:
            repo = self._repo_class(db)
            templates, _ = repo.get_all(keyword=keyword, page=1, page_size=100)
            return [t.to_dict() for t in templates]
        finally:
            db.close()


# 全局模板服务实例
_template_service: Optional[TemplateService] = None


def get_template_service() -> TemplateService:
    """获取模板服务单例"""
    global _template_service
    if _template_service is None:
        _template_service = TemplateService()
    return _template_service
