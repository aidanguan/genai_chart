import sqlite3
import json

conn = sqlite3.connect('infographic.db')
cursor = conn.cursor()

# 查询所有金字塔相关模板
cursor.execute("""
    SELECT id, name, description, design_config 
    FROM templates 
    WHERE id LIKE '%pyramid%' OR name LIKE '%金字塔%'
""")

print("=" * 80)
print("金字塔相关模板:")
print("=" * 80)

for row in cursor.fetchall():
    template_id, name, description, design_config = row
    print(f"\nID: {template_id}")
    print(f"名称: {name}")
    print(f"描述: {description}")
    print(f"配置: {design_config}")
    
    # 解析配置
    try:
        config = json.loads(design_config)
        print(f"结构类型: {config.get('design', {}).get('structure', {}).get('type')}")
        print(f"Items配置: {config.get('design', {}).get('items')}")
        print(f"Item配置: {config.get('design', {}).get('item')}")
    except:
        pass
    print("-" * 80)

# 查询所有层级类模板
cursor.execute("""
    SELECT id, name, category 
    FROM templates 
    WHERE category = 'hierarchy'
""")

print("\n\n所有层级类模板:")
print("=" * 80)
for row in cursor.fetchall():
    print(f"ID: {row[0]}, 名称: {row[1]}")

conn.close()
