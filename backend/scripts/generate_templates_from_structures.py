"""
从AntV结构自动生成模板配置
快速扩展模板库到50+
"""
import json
import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 结构到分类的映射
STRUCTURE_TO_CATEGORY_MAP = {
    # 列表类
    'list-row': 'list',
    'list-column': 'list',
    'list-grid': 'list',
    'list-pyramid': 'hierarchy',
    'list-sector': 'list',
    'list-waterfall': 'list',
    
    # 顺序类
    'sequence-steps': 'sequence',
    'sequence-zigzag-steps': 'sequence',
    'sequence-horizontal-zigzag': 'sequence',
    'sequence-timeline': 'sequence',
    'sequence-circular': 'sequence',
    'sequence-circle-arrows': 'sequence',
    'sequence-ascending-steps': 'sequence',
    'sequence-ascending-stairs-3d': 'sequence',
    'sequence-snake-steps': 'sequence',
    'sequence-color-snake-steps': 'sequence',
    'sequence-mountain': 'sequence',
    'sequence-pyramid': 'sequence',
    'sequence-roadmap-vertical': 'sequence',
    'sequence-cylinders-3d': 'sequence',
    'sequence-filter-mesh': 'sequence',
    'sequence-zigzag-pucks-3d': 'sequence',
    
    # 对比类
    'compare-binary-horizontal': 'comparison',
    'compare-hierarchy-left-right': 'comparison',
    'compare-hierarchy-row': 'comparison',
    
    # 层级类
    'hierarchy-tree': 'hierarchy',
    
    # 关系类
    'relation-circle': 'relation',
    'relation-network': 'relation',
    
    # 图表类
    'chart-column': 'chart',
    
    # 四象限类
    'quadrant': 'quadrant',
}


# 模板元数据 (中文名称、描述、适用场景、标签)
TEMPLATE_METADATA = {
    # 列表类
    'list-grid': {
        'name': '网格列表',
        'description': '网格布局展示多个项目,适合平铺展示',
        'use_cases': '产品展示、团队成员、功能特性、服务模块',
        'tags': ['网格', '列表', '平铺', '卡片'],
        'sort_order': 78
    },
    'list-sector': {
        'name': '扇形列表',
        'description': '扇形分布的列表布局,视觉效果独特',
        'use_cases': '服务介绍、产品分类、特性展示、环形菜单',
        'tags': ['扇形', '列表', '放射', '圆形'],
        'sort_order': 77
    },
    'list-waterfall': {
        'name': '瀑布流列表',
        'description': '瀑布流式布局,高度自适应',
        'use_cases': '图片展示、内容流、社交动态',
        'tags': ['瀑布流', '列表', '自适应'],
        'sort_order': 76
    },
    
    # 顺序类 - 高优先级
    'sequence-circular': {
        'name': '环形流程',
        'description': '环形循环布局,强调周期性和循环性',
        'use_cases': '生命周期、循环流程、PDCA循环、迭代过程',
        'tags': ['环形', '循环', '流程', '周期'],
        'sort_order': 95
    },
    'sequence-ascending-steps': {
        'name': '上升步骤',
        'description': '阶梯上升布局,展示进阶或递进关系',
        'use_cases': '成长路径、学习进阶、职业发展、等级制度',
        'tags': ['上升', '阶梯', '进阶', '成长'],
        'sort_order': 94
    },
    'sequence-roadmap-vertical': {
        'name': '垂直路线图',
        'description': '垂直方向的路线图布局',
        'use_cases': '产品路线图、项目规划、发展路径',
        'tags': ['路线图', '规划', '垂直', '时间线'],
        'sort_order': 93
    },
    'sequence-timeline': {
        'name': '标准时间轴',
        'description': '经典时间轴布局,展示时间序列事件',
        'use_cases': '历史事件、项目时间线、发展历程',
        'tags': ['时间轴', '历史', '时间线'],
        'sort_order': 92
    },
    'sequence-snake-steps': {
        'name': '蛇形步骤',
        'description': 'S形蛇形布局,适合长流程展示',
        'use_cases': '复杂流程、多步骤操作、工艺流程',
        'tags': ['蛇形', '流程', 'S形'],
        'sort_order': 91
    },
    'sequence-steps': {
        'name': '简单步骤',
        'description': '最简单的步骤流程图',
        'use_cases': '操作指南、简单流程、入门教程',
        'tags': ['步骤', '流程', '简单'],
        'sort_order': 88
    },
    'sequence-horizontal-zigzag': {
        'name': '横向Z字形',
        'description': '横向Z字形布局,节省空间',
        'use_cases': '工作流程、业务流程、操作步骤',
        'tags': ['Z字形', '横向', '流程'],
        'sort_order': 87
    },
    'sequence-mountain': {
        'name': '山峰型流程',
        'description': '山峰起伏型布局,视觉冲击力强',
        'use_cases': '挑战历程、项目阶段、发展波动',
        'tags': ['山峰', '起伏', '视觉'],
        'sort_order': 86
    },
    'sequence-pyramid': {
        'name': '金字塔流程',
        'description': '金字塔型流程布局',
        'use_cases': '层层递进、汇聚流程、收敛过程',
        'tags': ['金字塔', '流程', '递进'],
        'sort_order': 85
    },
    'sequence-color-snake-steps': {
        'name': '彩色蛇形步骤',
        'description': '彩色蛇形布局,视觉丰富',
        'use_cases': '多阶段流程、彩色分类流程',
        'tags': ['彩色', '蛇形', '流程'],
        'sort_order': 84
    },
    'sequence-circle-arrows': {
        'name': '圆形箭头流程',
        'description': '圆形布局带箭头连接',
        'use_cases': '循环流程、闭环系统、反馈机制',
        'tags': ['圆形', '箭头', '循环'],
        'sort_order': 83
    },
    'sequence-ascending-stairs-3d': {
        'name': '3D上升阶梯',
        'description': '3D立体上升阶梯效果',
        'use_cases': '进阶路径、等级体系、立体展示',
        'tags': ['3D', '阶梯', '立体'],
        'sort_order': 82
    },
    'sequence-cylinders-3d': {
        'name': '3D圆柱体流程',
        'description': '3D圆柱体布局,立体感强',
        'use_cases': '数据处理流程、系统架构',
        'tags': ['3D', '圆柱', '立体'],
        'sort_order': 81
    },
    'sequence-filter-mesh': {
        'name': '过滤网格流程',
        'description': '网格过滤式流程布局',
        'use_cases': '筛选流程、过滤系统、分层处理',
        'tags': ['过滤', '网格', '筛选'],
        'sort_order': 79
    },
    'sequence-zigzag-pucks-3d': {
        'name': '3D曲棍球流程',
        'description': '3D曲棍球式布局,创意独特',
        'use_cases': '创意展示、游戏流程',
        'tags': ['3D', '创意', '独特'],
        'sort_order': 78
    },
    
    # 第二批新增元数据
    'sequence-circle-arrows': {
        'name': '圆形箭头流程',
        'description': '圆形布局带箭头连接,强调循环和流转',
        'use_cases': '循环流程、闭环系统、反馈机制、迭代开发',
        'tags': ['圆形', '箭头', '循环', '闭环'],
        'sort_order': 89
    },
    'sequence-filter-mesh': {
        'name': '过滤网格流程',
        'description': '网格过滤式流程布局,展示筛选过程',
        'use_cases': '筛选流程、过滤系统、分层处理、漏斗模型',
        'tags': ['过滤', '网格', '筛选', '漏斗'],
        'sort_order': 83
    },
    'list-row': {
        'name': '横向列表(基础)',
        'description': '横向排列的基础列表布局',
        'use_cases': '简单列举、横向步骤、选项展示',
        'tags': ['横向', '列表', '简单', '基础'],
        'sort_order': 74
    },
    
    # 对比类
    'compare-binary-horizontal': {
        'name': '横向二元对比',
        'description': '左右二元对比布局',
        'use_cases': '方案选择、AB对比、优缺点分析',
        'tags': ['对比', '二元', '左右'],
        'sort_order': 72
    },
    'compare-hierarchy-left-right': {
        'name': '左右层级对比',
        'description': '左右两侧的层级对比',
        'use_cases': '复杂对比、多层级分析',
        'tags': ['对比', '层级', '左右'],
        'sort_order': 71
    },
    'compare-hierarchy-row': {
        'name': '行层级对比',
        'description': '行式层级对比布局',
        'use_cases': '分类对比、多维度对比',
        'tags': ['对比', '层级', '行式'],
        'sort_order': 70
    },
    
    # 关系类
    'relation-circle': {
        'name': '圆形关系图',
        'description': '圆形布局的关系网络',
        'use_cases': '中心辐射关系、核心关联、生态系统',
        'tags': ['关系', '圆形', '网络'],
        'sort_order': 68
    },
    'relation-network': {
        'name': '网络关系图',
        'description': '网状关系布局',
        'use_cases': '复杂关系网、社交网络、依赖关系',
        'tags': ['关系', '网络', '复杂'],
        'sort_order': 67
    },
}


# 数据Schema模板
SCHEMA_TEMPLATES = {
    'list_simple': {
        "description": "简单列表数据",
        "dataFields": {
            "title": {"type": "string", "required": False, "description": "标题"},
            "desc": {"type": "string", "required": False, "description": "描述"},
            "items": {
                "type": "array",
                "required": True,
                "description": "数据项列表",
                "itemSchema": {
                    "label": {"type": "string", "required": True, "description": "项目标题"},
                    "desc": {"type": "string", "required": False, "description": "项目描述"}
                }
            }
        }
    },
    'sequence_simple': {
        "description": "顺序流程数据",
        "dataFields": {
            "title": {"type": "string", "required": False, "description": "标题"},
            "desc": {"type": "string", "required": False, "description": "描述"},
            "items": {
                "type": "array",
                "required": True,
                "description": "流程步骤列表",
                "itemSchema": {
                    "label": {"type": "string", "required": True, "description": "步骤名称"},
                    "desc": {"type": "string", "required": False, "description": "步骤描述"}
                }
            }
        }
    },
    'comparison_binary': {
        "description": "二元对比数据",
        "dataFields": {
            "title": {"type": "string", "required": False, "description": "标题"},
            "left": {
                "type": "object",
                "required": True,
                "description": "左侧数据",
                "schema": {
                    "title": {"type": "string", "required": True, "description": "左侧标题"},
                    "items": {"type": "array", "required": True, "description": "左侧项目"}
                }
            },
            "right": {
                "type": "object",
                "required": True,
                "description": "右侧数据",
                "schema": {
                    "title": {"type": "string", "required": True, "description": "右侧标题"},
                    "items": {"type": "array", "required": True, "description": "右侧项目"}
                }
            }
        }
    },
    'relation_simple': {
        "description": "关系网络数据",
        "dataFields": {
            "title": {"type": "string", "required": False, "description": "标题"},
            "center": {"type": "string", "required": True, "description": "中心节点"},
            "nodes": {
                "type": "array",
                "required": True,
                "description": "节点列表",
                "itemSchema": {
                    "label": {"type": "string", "required": True, "description": "节点名称"},
                    "desc": {"type": "string", "required": False, "description": "节点描述"}
                }
            }
        }
    }
}


def generate_template_config(structure_type: str) -> Dict[str, Any]:
    """
    根据structure类型生成模板配置
    
    Args:
        structure_type: AntV结构类型,如 'list-grid'
    
    Returns:
        完整的模板配置字典
    """
    if structure_type not in STRUCTURE_TO_CATEGORY_MAP:
        logger.warning(f"未知结构类型: {structure_type}")
        return None
    
    category = STRUCTURE_TO_CATEGORY_MAP[structure_type]
    metadata = TEMPLATE_METADATA.get(structure_type)
    
    if not metadata:
        logger.warning(f"缺少元数据: {structure_type}")
        return None
    
    # 选择合适的Schema模板
    if category in ['list', 'hierarchy']:
        schema_template = SCHEMA_TEMPLATES['list_simple']
    elif category == 'sequence':
        schema_template = SCHEMA_TEMPLATES['sequence_simple']
    elif category == 'comparison':
        schema_template = SCHEMA_TEMPLATES['comparison_binary']
    elif category == 'relation':
        schema_template = SCHEMA_TEMPLATES['relation_simple']
    else:
        schema_template = SCHEMA_TEMPLATES['list_simple']
    
    # 生成模板配置
    template_config = {
        "id": structure_type,
        "name": metadata['name'],
        "category": category,
        "structure_type": structure_type,
        "description": metadata['description'],
        "keywords": ','.join(metadata['tags']),
        "use_cases": metadata['use_cases'],
        "preview_url": "",
        "data_schema": schema_template,
        "design_config": {
            "design": {
                "structure": {"type": structure_type},
                "title": "default",
                "item": "simple"
            }
        },
        "tags": metadata['tags'],
        "sort_order": metadata['sort_order'],
        "is_active": True
    }
    
    return template_config


def generate_batch_templates(structure_types: List[str]) -> List[Dict[str, Any]]:
    """
    批量生成模板配置
    
    Args:
        structure_types: 结构类型列表
    
    Returns:
        模板配置列表
    """
    templates = []
    
    for structure_type in structure_types:
        config = generate_template_config(structure_type)
        if config:
            templates.append(config)
            logger.info(f"✓ 生成模板: {structure_type} - {config['name']}")
        else:
            logger.error(f"✗ 跳过模板: {structure_type}")
    
    return templates


def generate_batch1():
    """生成第一批: 高优先级模板"""
    high_priority_structures = [
        # 顺序类 (10个)
        'sequence-circular',
        'sequence-ascending-steps',
        'sequence-roadmap-vertical',
        'sequence-timeline',
        'sequence-snake-steps',
        'sequence-steps',
        'sequence-horizontal-zigzag',
        'sequence-mountain',
        'sequence-pyramid',
        'sequence-color-snake-steps',
        
        # 列表类 (3个)
        'list-grid',
        'list-sector',
        'list-waterfall',
        
        # 对比类 (3个)
        'compare-binary-horizontal',
        'compare-hierarchy-left-right',
        'compare-hierarchy-row',
        
        # 关系类 (2个)
        'relation-circle',
        'relation-network',
        
        # 3D视觉 (2个)
        'sequence-ascending-stairs-3d',
        'sequence-cylinders-3d',
    ]
    
    logger.info(f"\n第一批: 高优先级模板 ({len(high_priority_structures)}个)")
    return generate_batch_templates(high_priority_structures), "templates_batch1_high_priority.json"


def generate_batch2():
    """生成第二批: 中优先级模板"""
    medium_priority_structures = [
        # 顺序类创意模板 (3个)
        'sequence-circle-arrows',      # 圆形箭头流程
        'sequence-filter-mesh',        # 过滤网格流程  
        'sequence-zigzag-pucks-3d',    # 3D曲棍球流程
        
        # 列表类变体 (1个)
        'list-row',                    # 横向列表(基础版)
    ]
    
    logger.info(f"\n第二批: 中优先级模板 ({len(medium_priority_structures)}个)")
    return generate_batch_templates(medium_priority_structures), "templates_batch2_medium_priority.json"


def generate_batch3():
    """生成第三批: 补充完善模板库"""
    supplementary_structures = [
        # 对比类补充 (2个)
        'compare-binary-horizontal',  # 注意: 这个已存在,但我们用不同配置创建变体
        
        # 层级类补充 - hierarchy-tree的不同变体暂时跳过,需要特殊处理
        
        # 关系类补充 (暂无新结构)
        
        # 其他可用结构 - 从AntV源码发现的
        # 注意: 有些结构可能需要特殊的数据格式,我们先添加确定可用的
    ]
    
    # 由于发现可直接使用的新结构较少,我们采用另一种策略:
    # 为现有结构创建不同的item组合,形成新模板变体
    
    logger.info(f"\n第三批: 补充完善模板库")
    logger.info("策略: 创建现有结构的高价值变体")
    
    # 暂时返回空列表,需要手动配置变体
    return [], "templates_batch3_supplementary.json"


def main():
    """主函数"""
    import sys
    
    logger.info("="*60)
    logger.info("开始生成扩展模板配置")
    logger.info("="*60)
    
    # 检查命令行参数
    batch = sys.argv[1] if len(sys.argv) > 1 else "3"
    
    if batch == "1":
        templates, output_file = generate_batch1()
    elif batch == "2":
        templates, output_file = generate_batch2()
    elif batch == "3":
        templates, output_file = generate_batch3()
    else:
        logger.error(f"未知批次: {batch}")
        logger.info("用法: python generate_templates_from_structures.py [1|2|3]")
        logger.info("  1 - 生成第一批(高优先级,20个)")
        logger.info("  2 - 生成第二批(中优先级,4个)")
        logger.info("  3 - 生成第三批(补充完善,创建变体)")
        return
    
    # 按分类统计
    category_count = {}
    for template in templates:
        category = template['category']
        category_count[category] = category_count.get(category, 0) + 1
    
    logger.info(f"\n分类统计:")
    for category, count in category_count.items():
        logger.info(f"  {category}: {count}个")
    
    # 保存到JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(templates, f, ensure_ascii=False, indent=2)
    
    logger.info(f"\n✅ 成功生成 {len(templates)} 个模板")
    logger.info(f"📁 保存到: {output_file}")
    logger.info(f"\n下一步:")
    logger.info(f"  1. 检查生成的配置: cat {output_file}")
    logger.info(f"  2. 导入数据库: python scripts/import_templates.py {output_file}")
    logger.info(f"  3. 配置Dify工作流: 编辑 app/config/dify_workflows.yaml")
    logger.info("="*60)


if __name__ == "__main__":
    main()
