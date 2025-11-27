import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal
from app.models import Template
import json

def fix_template():
    db = SessionLocal()
    try:
        # 查找 sequence-steps-numbered 模板
        template = db.query(Template).filter(Template.id == 'sequence-steps-numbered').first()
        
        if not template:
            print("模板 sequence-steps-numbered 不存在")
            return
        
        # 解析当前配置
        config = json.loads(template.design_config)
        
        # 显示当前配置
        print(f"当前配置: {json.dumps(config, indent=2, ensure_ascii=False)}")
        
        # 修改 item
        config['design']['item'] = 'indexed-card'
        
        # 更新数据库
        template.design_config = json.dumps(config, ensure_ascii=False)
        db.commit()
        
        print(f"\n✅ 成功更新模板 sequence-steps-numbered")
        print(f"新配置: {json.dumps(config, indent=2, ensure_ascii=False)}")
        
    except Exception as e:
        print(f"错误: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_template()
