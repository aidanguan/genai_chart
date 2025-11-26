"""
模板数据爬取和整理脚本
从AntV Infographic官网爬取模板信息
"""
import json
import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 7大分类定义
CATEGORIES = {
    "chart": {"name": "图表型", "description": "数值展示,柱状图等可视化图表"},
    "comparison": {"name": "对比型", "description": "优劣对比、SWOT分析"},
    "hierarchy": {"name": "层级型", "description": "组织结构、分类信息"},
    "list": {"name": "列表型", "description": "步骤说明、清单、简单信息罗列"},
    "quadrant": {"name": "四象限型", "description": "市场定位、风险评估"},
    "relation": {"name": "关系型", "description": "关系网络、关联分析"},
    "sequence": {"name": "顺序型", "description": "时间线、流程图、递进关系"}
}


def create_initial_templates() -> List[Dict[str, Any]]:
    """
    创建初始模板数据
    TODO: 后续从官网爬取完整的100个模板
    目前先创建基础模板数据
    """
    templates = [
        # 顺序型模板
        {
            "id": "list-row-horizontal-icon-arrow",
            "name": "图标横向流程图",
            "category": "sequence",
            "description": "带图标和箭头的横向流程图,视觉效果丰富",
            "use_cases": "产品流程、服务流程、工作流程",
            "preview_url": "",
            "data_schema": {
                "description": "横向流程图,带图标和箭头",
                "dataFields": {
                    "title": {"type": "string", "required": False, "description": "标题"},
                    "desc": {"type": "string", "required": False, "description": "描述"},
                    "items": {
                        "type": "array",
                        "required": True,
                        "description": "流程步骤列表",
                        "itemSchema": {
                            "label": {"type": "string", "required": True, "description": "步骤名称"},
                            "desc": {"type": "string", "required": False, "description": "步骤描述"},
                            "icon": {"type": "string", "required": False, "description": "图标,格式:icon:mdi/iconname"}
                        }
                    }
                }
            },
            "design_config": {
                "template": "list-row-horizontal-icon-arrow"
            },
            "tags": ["流程", "横向", "图标", "箭头"],
            "sort_order": 100
        },
        {
            "id": "timeline-horizontal",
            "name": "横向时间轴",
            "category": "sequence",
            "description": "横向时间轴布局,适合展示发展历程",
            "use_cases": "公司发展史、项目里程碑、产品迭代历程",
            "preview_url": "",
            "data_schema": {
                "description": "横向时间轴",
                "dataFields": {
                    "title": {"type": "string", "required": False},
                    "items": {
                        "type": "array",
                        "required": True,
                        "itemSchema": {
                            "time": {"type": "string", "required": True, "description": "时间点"},
                            "title": {"type": "string", "required": True, "description": "事件标题"},
                            "desc": {"type": "string", "required": False, "description": "事件描述"}
                        }
                    }
                }
            },
            "design_config": {
                "design": {
                    "structure": {"type": "timeline-horizontal"},
                    "title": "default"
                }
            },
            "tags": ["时间轴", "历程", "里程碑"],
            "sort_order": 90
        },
        # 列表型模板
        {
            "id": "list-column-simple",
            "name": "简单纵向列表",
            "category": "list",
            "description": "纵向列表布局,适合展示要点清单",
            "use_cases": "操作步骤、注意事项、要点罗列",
            "preview_url": "",
            "data_schema": {
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
            },
            "design_config": {
                "design": {
                    "structure": {"type": "list-column"},
                    "title": "default",
                    "item": "simple"
                }
            },
            "tags": ["列表", "纵向", "清单"],
            "sort_order": 80
        },
        {
            "id": "checklist",
            "name": "检查清单",
            "category": "list",
            "description": "带复选框的检查清单",
            "use_cases": "任务清单、检查项、待办事项",
            "preview_url": "",
            "data_schema": {
                "description": "检查清单",
                "dataFields": {
                    "title": {"type": "string", "required": False},
                    "items": {
                        "type": "array",
                        "required": True,
                        "itemSchema": {
                            "label": {"type": "string", "required": True},
                            "checked": {"type": "boolean", "required": False, "description": "是否已完成"}
                        }
                    }
                }
            },
            "design_config": {
                "design": {
                    "structure": {"type": "list-checklist"},
                    "title": "default"
                }
            },
            "tags": ["清单", "检查", "任务"],
            "sort_order": 75
        },
        # 层级型模板
        {
            "id": "pyramid-layer",
            "name": "金字塔层级图",
            "category": "hierarchy",
            "description": "金字塔型布局,展示层级结构",
            "use_cases": "优先级展示、层级结构、组织架构",
            "preview_url": "",
            "data_schema": {
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
            },
            "design_config": {
                "design": {
                    "structure": {"type": "list-pyramid"},
                    "title": "default",
                    "items": [{"type": "badge-card"}]
                }
            },
            "tags": ["金字塔", "层级", "优先级"],
            "sort_order": 70
        },
        {
            "id": "org-tree",
            "name": "组织架构树",
            "category": "hierarchy",
            "description": "树形组织结构图",
            "use_cases": "公司架构、部门结构、团队组成",
            "preview_url": "",
            "data_schema": {
                "description": "组织架构树",
                "dataFields": {
                    "title": {"type": "string", "required": False},
                    "root": {
                        "type": "object",
                        "required": True,
                        "description": "根节点",
                        "schema": {
                            "name": {"type": "string", "required": True},
                            "position": {"type": "string", "required": False},
                            "children": {"type": "array", "required": False}
                        }
                    }
                }
            },
            "design_config": {
                "design": {
                    "structure": {"type": "tree-org"},
                    "title": "default"
                }
            },
            "tags": ["组织", "架构", "树形"],
            "sort_order": 65
        },
        # 对比型模板
        {
            "id": "comparison-two-column",
            "name": "双栏对比",
            "category": "comparison",
            "description": "左右双栏对比展示",
            "use_cases": "产品对比、方案对比、优劣分析",
            "preview_url": "",
            "data_schema": {
                "description": "双栏对比",
                "dataFields": {
                    "title": {"type": "string", "required": False},
                    "left": {
                        "type": "object",
                        "required": True,
                        "schema": {
                            "title": {"type": "string", "required": True},
                            "items": {"type": "array", "required": True}
                        }
                    },
                    "right": {
                        "type": "object",
                        "required": True,
                        "schema": {
                            "title": {"type": "string", "required": True},
                            "items": {"type": "array", "required": True}
                        }
                    }
                }
            },
            "design_config": {
                "design": {
                    "structure": {"type": "comparison-column"},
                    "title": "default"
                }
            },
            "tags": ["对比", "双栏", "比较"],
            "sort_order": 60
        },
        {
            "id": "swot-analysis",
            "name": "SWOT分析",
            "category": "comparison",
            "description": "SWOT四象限分析图",
            "use_cases": "优势劣势分析、机会威胁分析、战略分析",
            "preview_url": "",
            "data_schema": {
                "description": "SWOT分析",
                "dataFields": {
                    "title": {"type": "string", "required": False},
                    "strengths": {"type": "array", "required": True, "description": "优势"},
                    "weaknesses": {"type": "array", "required": True, "description": "劣势"},
                    "opportunities": {"type": "array", "required": True, "description": "机会"},
                    "threats": {"type": "array", "required": True, "description": "威胁"}
                }
            },
            "design_config": {
                "design": {
                    "structure": {"type": "quadrant-swot"},
                    "title": "default"
                }
            },
            "tags": ["SWOT", "分析", "四象限"],
            "sort_order": 55
        },
        # 四象限型模板
        {
            "id": "matrix-2x2",
            "name": "2x2矩阵",
            "category": "quadrant",
            "description": "经典2x2矩阵图",
            "use_cases": "优先级矩阵、波士顿矩阵、风险评估",
            "preview_url": "",
            "data_schema": {
                "description": "2x2矩阵",
                "dataFields": {
                    "title": {"type": "string", "required": False},
                    "xAxis": {"type": "string", "required": True, "description": "横轴标签"},
                    "yAxis": {"type": "string", "required": True, "description": "纵轴标签"},
                    "quadrants": {
                        "type": "array",
                        "required": True,
                        "description": "四个象限数据",
                        "itemSchema": {
                            "label": {"type": "string", "required": True},
                            "items": {"type": "array", "required": False}
                        }
                    }
                }
            },
            "design_config": {
                "design": {
                    "structure": {"type": "matrix-2x2"},
                    "title": "default"
                }
            },
            "tags": ["矩阵", "象限", "优先级"],
            "sort_order": 50
        },
        # 关系型模板
        {
            "id": "mindmap-radial",
            "name": "放射状思维导图",
            "category": "relation",
            "description": "中心放射状关系图",
            "use_cases": "思维导图、关联分析、概念地图",
            "preview_url": "",
            "data_schema": {
                "description": "放射状思维导图",
                "dataFields": {
                    "center": {"type": "string", "required": True, "description": "中心主题"},
                    "branches": {
                        "type": "array",
                        "required": True,
                        "description": "分支",
                        "itemSchema": {
                            "label": {"type": "string", "required": True},
                            "children": {"type": "array", "required": False}
                        }
                    }
                }
            },
            "design_config": {
                "design": {
                    "structure": {"type": "mindmap-radial"},
                    "title": "default"
                }
            },
            "tags": ["思维导图", "关系", "放射"],
            "sort_order": 45
        },
        # 图表型模板
        {
            "id": "bar-chart-vertical",
            "name": "垂直柱状图",
            "category": "chart",
            "description": "垂直方向的柱状图",
            "use_cases": "数据对比、销售统计、指标展示",
            "preview_url": "",
            "data_schema": {
                "description": "垂直柱状图",
                "dataFields": {
                    "title": {"type": "string", "required": False},
                    "data": {
                        "type": "array",
                        "required": True,
                        "itemSchema": {
                            "label": {"type": "string", "required": True, "description": "类别名称"},
                            "value": {"type": "number", "required": True, "description": "数值"}
                        }
                    }
                }
            },
            "design_config": {
                "design": {
                    "structure": {"type": "chart-bar-vertical"},
                    "title": "default"
                }
            },
            "tags": ["柱状图", "数据", "图表"],
            "sort_order": 40
        }
    ]
    
    return templates


def main():
    """主函数"""
    logger.info("开始整理模板数据...")
    
    # 创建初始模板数据
    templates = create_initial_templates()
    
    logger.info(f"已整理 {len(templates)} 个模板")
    
    # 按分类统计
    category_count = {}
    for template in templates:
        category = template["category"]
        category_count[category] = category_count.get(category, 0) + 1
    
    logger.info("分类统计:")
    for category_code, count in category_count.items():
        category_name = CATEGORIES[category_code]["name"]
        logger.info(f"  {category_name} ({category_code}): {count}个")
    
    # 保存到JSON文件
    output_file = "templates_initial.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(templates, f, ensure_ascii=False, indent=2)
    
    logger.info(f"\n✅ 模板数据已保存到: {output_file}")
    logger.info(f"📝 注意: 这是初始的11个模板,后续需要从官网爬取完整的100个模板")


if __name__ == "__main__":
    main()
