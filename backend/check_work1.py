import sqlite3
import json

conn = sqlite3.connect('infographic.db')
cursor = conn.cursor()

# 检查表结构
cursor.execute('PRAGMA table_info(user_works)')
cols = cursor.fetchall()
print('=== 表结构 ===')
for c in cols:
    print(f'{c[1]} ({c[2]})')

print('\n=== 作品1数据 ===')
cursor.execute('SELECT * FROM user_works WHERE id=1')
row = cursor.fetchone()

if row:
    col_names = [desc[0] for desc in cursor.description]
    for i, col_name in enumerate(col_names):
        value = row[i]
        if col_name == 'design_data' and value:
            try:
                design = json.loads(value)
                print(f'{col_name}:')
                print(json.dumps(design, indent=2, ensure_ascii=False)[:1000])
            except:
                print(f'{col_name}: {value[:200] if value else None}')
        else:
            print(f'{col_name}: {value}')
else:
    print('作品1不存在')

conn.close()
