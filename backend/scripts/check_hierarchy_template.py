"""检查左右层级对比模板"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.db import get_db
from app.models.template import Template

def check_template():
    with get_db() as db:
        templates = db.query(Template).filter(
            Template.category == 'comparison'
        ).all()
        
        print(f"找到 {len(templates)} 个对比型模板:\n")
        for t in templates:
            print(f"ID: {t.id}")
            print(f"名称: {t.name}")
            print(f"分类: {t.category}")
            print(f"包含'compare': {'compare' in t.id}")
            if 'hierarchy' in t.id and 'left' in t.id:
                print(f"\ndesign_config:")
                print(json.dumps(t.design_config, ensure_ascii=False, indent=2))
            print("="*60)

if __name__ == "__main__":
    check_template()
