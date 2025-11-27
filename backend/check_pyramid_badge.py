import sqlite3
import json

# 连接数据库
conn = sqlite3.connect('infographic.db')
cursor = conn.cursor()

# 查询模板
cursor.execute("SELECT id, name, design_config FROM templates WHERE id = 'list-pyramid-badge'")
result = cursor.fetchone()

if result:
    template_id, name, design_config_str = result
    print(f"Template ID: {template_id}")
    print(f"Name: {name}")
    print(f"Design Config:")
    design_config = json.loads(design_config_str)
    print(json.dumps(design_config, indent=2, ensure_ascii=False))
else:
    print("Template not found")

conn.close()
