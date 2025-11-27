import sqlite3
import json

# 连接数据库
conn = sqlite3.connect('infographic.db')
cursor = conn.cursor()

# 正确的配置格式
correct_config = {
    "design": {
        "structure": {
            "type": "list-pyramid"
        },
        "title": "default",
        "items": [{"type": "badge-card"}]
    }
}

# 更新模板配置
cursor.execute(
    "UPDATE templates SET design_config = ? WHERE id = ?",
    (json.dumps(correct_config, ensure_ascii=False), 'list-pyramid-badge')
)

conn.commit()
print(f"Updated {cursor.rowcount} rows")

# 验证更新
cursor.execute("SELECT id, name, design_config FROM templates WHERE id = 'list-pyramid-badge'")
result = cursor.fetchone()

if result:
    template_id, name, design_config_str = result
    print(f"\nVerification:")
    print(f"Template ID: {template_id}")
    print(f"Name: {name}")
    print(f"Design Config:")
    design_config = json.loads(design_config_str)
    print(json.dumps(design_config, indent=2, ensure_ascii=False))

conn.close()
