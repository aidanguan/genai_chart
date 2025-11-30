import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.utils.db import get_db_session
from app.models.template import Template

db = get_db_session()
try:
    # 查询数据库中需要的模板
    template_ids = ['sequence-circular', 'sequence-circle-arrows', 'sequence-circular-icon']
    
    for tid in template_ids:
        template = db.query(Template).filter(Template.id == tid).first()
        if template:
            print(f'✓ 找到模板: {tid}')
            print(f'  名称: {template.name}')
            print(f'  类型: {template.category}')
        else:
            print(f'✗ 未找到模板: {tid}')
        print()
finally:
    db.close()
