"""
模板分类初始化脚本
从AntV Infographic的built-in.ts读取所有模板并自动分类
"""
import sys
import os
import re
import json
from pathlib import Path
from typing import Dict, List, Any

# 添加项目根目录到路径
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.utils.db import get_db_session
from sqlalchemy import text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def classify_template(template_id: str, structure_type: str) -> str:
    """
    根据structure_type自动分类模板
    
    Args:
        template_id: 模板ID
        structure_type: structure类型
    
    Returns:
        str: 分类代码 (chart/comparison/hierarchy/list/quadrant/relationship/sequence)
    """
    if structure_type.startswith('chart-'):
        return 'chart'
    elif structure_type.startswith('compare-'):
        return 'comparison'
    elif structure_type.startswith('hierarchy-') or structure_type == 'list-pyramid':
        return 'hierarchy'
    elif structure_type.startswith('list-'):
        return 'list'
    elif structure_type == 'quadrant':
        return 'quadrant'
    elif structure_type.startswith('relation-'):
        return 'relationship'
    elif structure_type.startswith('sequence-'):
        return 'sequence'
    else:
        # 默认根据template_id判断
        if 'pyramid' in template_id:
            return 'hierarchy'
        elif 'quadrant' in template_id or 'matrix' in template_id:
            return 'quadrant'
        elif 'compare' in template_id or 'swot' in template_id:
            return 'comparison'
        elif 'sequence' in template_id or 'timeline' in template_id or 'steps' in template_id:
            return 'sequence'
        elif 'relation' in template_id:
            return 'relationship'
        else:
            return 'list'  # 默认分类


def extract_structure_type_from_design(design_config: Dict[str, Any]) -> str:
    """
    从design配置中提取structure type
    
    Args:
        design_config: design配置对象
    
    Returns:
        str: structure类型
    """
    if not design_config:
        return ""
    
    structure = design_config.get('structure', {})
    if isinstance(structure, dict):
        return structure.get('type', '')
    elif isinstance(structure, str):
        return structure
    
    return ""


def update_template_categories():
    """
    更新数据库中所有模板的category和structure_type
    """
    logger.info("开始更新模板分类...")
    
    db = get_db_session()
    try:
        # 获取所有模板
        query = text("SELECT id, design_config FROM templates")
        result = db.execute(query).fetchall()
        
        logger.info(f"找到 {len(result)} 个模板需要分类")
        
        updated_count = 0
        for row in result:
            template_id = row[0]
            design_config = row[1]
            
            # 提取structure_type
            structure_type = extract_structure_type_from_design(design_config)
            
            # 自动分类
            category = classify_template(template_id, structure_type)
            
            # 更新数据库
            update_sql = text("""
                UPDATE templates 
                SET category = :category, 
                    structure_type = :structure_type
                WHERE id = :template_id
            """)
            
            db.execute(update_sql, {
                'category': category,
                'structure_type': structure_type,
                'template_id': template_id
            })
            
            updated_count += 1
            logger.info(f"✓ {template_id}: category={category}, structure_type={structure_type}")
        
        db.commit()
        logger.info(f"分类完成！共更新 {updated_count} 个模板")
        
    except Exception as e:
        db.rollback()
        logger.error(f"分类更新失败: {e}")
        raise
    finally:
        db.close()


def generate_category_statistics():
    """
    生成分类统计信息
    """
    logger.info("\n" + "="*60)
    logger.info("分类统计")
    logger.info("="*60)
    
    db = get_db_session()
    try:
        # 按category统计
        query = text("""
            SELECT category, COUNT(*) as count
            FROM templates
            GROUP BY category
            ORDER BY count DESC
        """)
        
        result = db.execute(query).fetchall()
        
        category_names = {
            'chart': '图表型',
            'comparison': '对比型',
            'hierarchy': '层级型',
            'list': '列表型',
            'quadrant': '四象限型',
            'relationship': '关系型',
            'sequence': '顺序型'
        }
        
        total = 0
        for row in result:
            category = row[0]
            count = row[1]
            total += count
            category_name = category_names.get(category, category)
            logger.info(f"{category_name} ({category}): {count} 个模板")
        
        logger.info(f"\n总计: {total} 个模板")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"统计失败: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    logger.info("模板分类初始化工具")
    logger.info("=" * 60)
    
    # 第一步：更新分类
    update_template_categories()
    
    # 第二步：生成统计
    generate_category_statistics()
    
    logger.info("\n✓ 所有操作完成！")
