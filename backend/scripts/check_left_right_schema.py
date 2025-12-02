"""检查左右层级对比模板的schema"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.db import get_db
from app.models.template import Template

def check_schema():
    with get_db() as db:
        template = db.query(Template).filter(
            Template.id == 'compare-hierarchy-left-right'
        ).first()
        
        if template:
            print(f"模板名称: {template.name}")
            print(f"模板ID: {template.id}")
            print(f"\ndata_schema:")
            print(json.dumps(template.data_schema, ensure_ascii=False, indent=2))
        else:
            print("未找到模板")

if __name__ == "__main__":
    check_schema()
