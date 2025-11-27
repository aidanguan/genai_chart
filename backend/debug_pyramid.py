import sqlite3
import json

conn = sqlite3.connect('infographic.db')
cursor = conn.cursor()

# 查询所有包含pyramid和badge的模板
cursor.execute("""
    SELECT id, name, design_config 
    FROM templates 
    WHERE id LIKE '%pyramid%' AND id LIKE '%badge%'
""")

results = cursor.fetchall()
print(f"找到 {len(results)} 个模板")
print("=" * 80)

for template_id, name, design_config_str in results:
    print(f"\nID: {template_id}")
    print(f"名称: {name}")
    print(f"配置:")
    try:
        config = json.loads(design_config_str)
        print(json.dumps(config, indent=2, ensure_ascii=False))
    except:
        print(design_config_str)
    print("-" * 80)

conn.close()
