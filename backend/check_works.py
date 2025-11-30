import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.utils.db import get_db_session
from app.models.work import UserWork

db = get_db_session()
try:
    works = db.query(UserWork).all()
    print(f'作品数量: {len(works)}')
    print()
    for w in works[:5]:
        print(f'ID={w.id}')
        print(f'  template_id={w.template_id}')
        print(f'  title={w.title}')
        print(f'  input_text={w.input_text[:50]}...')
        print()
finally:
    db.close()
