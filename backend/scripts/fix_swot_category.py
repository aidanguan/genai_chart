#!/usr/bin/env python3
"""
修复SWOT模板分类
将swot-analysis模板的分类从comparison改为quadrant
"""
import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from database import get_db
from models.template import Template

def fix_swot_category():
    """将swot-analysis模板的分类改为quadrant"""
    db = next(get_db())
    
    try:
        # 查询当前的swot-analysis模板
        template = db.query(Template).filter(Template.id == 'swot-analysis').first()
        
        if not template:
            print("❌ 未找到swot-analysis模板")
            return
        
        print(f"📋 当前模板信息:")
        print(f"   ID: {template.id}")
        print(f"   名称: {template.name}")
        print(f"   当前分类: {template.category}")
        
        # 更新分类为quadrant
        template.category = 'quadrant'
        db.commit()
        
        print(f"✅ 已将swot-analysis模板分类更新为: quadrant")
        
        # 验证更新
        updated_template = db.query(Template).filter(Template.id == 'swot-analysis').first()
        print(f"✓ 验证: {updated_template.category}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 更新失败: {e}")
        raise
    finally:
        db.close()

if __name__ == '__main__':
    fix_swot_category()
