import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.db import get_db_session
from app.models.template import Template
import json

db = get_db_session()
try:
    template_ids = ['compare-hierarchy-left-right', 'compare-hierarchy-row', 'relation-circle', 'relation-circle-connected', 'mindmap-radial']
    templates = db.query(Template).filter(Template.id.in_(template_ids)).all()
    
    for t in templates:
        print(f'\n{"="*50}')
        print(f'ID: {t.id}')
        print(f'Name: {t.name}')
        print(f'Category: {t.category}')
        print(f'Structure Type: {t.structure_type}')
        print(f'Design Config:')
        print(json.dumps(t.design_config, ensure_ascii=False, indent=2))
finally:
    db.close()
