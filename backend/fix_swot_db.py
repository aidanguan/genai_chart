import sys
sys.path.insert(0, '/app')

from sqlalchemy import create_engine, text

engine = create_engine('sqlite:////app/data/genai_chart.db')

with engine.connect() as conn:
    # 更新分类
    conn.execute(text("UPDATE templates SET category='quadrant' WHERE id='swot-analysis'"))
    conn.commit()
    
    # 验证更新
    result = conn.execute(text("SELECT id, name, category FROM templates WHERE id='swot-analysis'")).fetchone()
    if result:
        print(f"✅ 更新成功!")
        print(f"   ID: {result[0]}")
        print(f"   Name: {result[1]}")
        print(f"   Category: {result[2]}")
    else:
        print("❌ 未找到swot-analysis模板")
