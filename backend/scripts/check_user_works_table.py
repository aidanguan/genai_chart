"""检查user_works表结构"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.db import engine
from sqlalchemy import inspect, text

inspector = inspect(engine)
print('现有表:', inspector.get_table_names())

# 检查user_works表的列
if 'user_works' in inspector.get_table_names():
    columns = inspector.get_columns('user_works')
    print('\nuser_works表结构:')
    for col in columns:
        print(f"  {col['name']}: {col['type']} (nullable={col['nullable']}, autoincrement={col.get('autoincrement', 'N/A')})")
    
    # 检查是否需要删除并重新创建表
    print('\n✓ user_works表已存在，但可能结构不正确')
    print('建议: 删除并重新创建该表')
else:
    print('\n✗ user_works表不存在')
