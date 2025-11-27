"""检查模板schema"""
import sqlite3
import json

conn = sqlite3.connect('infographic.db')
cursor = conn.cursor()
cursor.execute('SELECT id, name, data_schema FROM templates WHERE id=?', ('bar-chart-vertical',))
result = cursor.fetchone()

if result:
    print(f"Template ID: {result[0]}")
    print(f"Template Name: {result[1]}")
    print(f"\nData Schema:")
    if result[2]:
        schema = json.loads(result[2])
        print(json.dumps(schema, ensure_ascii=False, indent=2))
    else:
        print("None")
else:
    print("Template not found")

conn.close()
