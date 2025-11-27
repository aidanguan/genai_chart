"""更新 sequence-zigzag-steps-underline-text 模板的 schema，添加 icon 字段"""
from app.utils.db import get_db_session
from app.models.template import Template
import json

def update_template():
    db = get_db_session()
    
    try:
        # 查找模板
        template = db.query(Template).filter(
            Template.id == 'sequence-zigzag-steps-underline-text'
        ).first()
        
        if not template:
            print(f"❌ 模板不存在: sequence-zigzag-steps-underline-text")
            return
        
        print(f"✅ 找到模板: {template.id}")
        print(f"当前 schema: {template.data_schema}")
        
        # 更新 schema
        new_schema = {
            'description': 'W型折线步骤图',
            'dataFields': {
                'title': {'type': 'string', 'required': False, 'description': '标题'},
                'desc': {'type': 'string', 'required': False, 'description': '描述'},
                'items': {
                    'type': 'array',
                    'required': True,
                    'description': '步骤列表',
                    'itemSchema': {
                        'label': {'type': 'string', 'required': True, 'description': '步骤名称'},
                        'desc': {'type': 'string', 'required': False, 'description': '步骤描述'},
                        'icon': {'type': 'string', 'required': False, 'description': '图标，格式：icon:集合名/图标名，如icon:mdi/check-circle'}
                    }
                }
            }
        }
        
        template.data_schema = json.dumps(new_schema)
        db.commit()
        print(f'✅ 模板 schema 已更新')
        print(f'新 schema: {template.data_schema}')
        
    except Exception as e:
        db.rollback()
        print(f'❌ 更新失败: {e}')
    finally:
        db.close()

if __name__ == '__main__':
    update_template()
