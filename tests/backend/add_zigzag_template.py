"""添加 sequence-zigzag-steps-underline-text 模板到数据库"""
from app.utils.db import get_db_session
from app.models.template import Template
import json

def add_template():
    db = get_db_session()
    
    try:
        # 检查是否已存在
        existing = db.query(Template).filter(
            Template.id == 'sequence-zigzag-steps-underline-text'
        ).first()
        
        if existing:
            print(f"模板已存在: {existing.id}")
            return
        
        template_data = {
            'id': 'sequence-zigzag-steps-underline-text',
            'name': '折线步骤图（下划线文字）',
            'category': 'sequence',
            'structure_type': 'sequence-zigzag-steps',
            'description': 'W型折线路径的步骤图，节点配光晕与装饰图案，文字带下划线效果',
            'keywords': '流程,步骤,折线,zigzag',
            'use_cases': '产品流程、服务流程、工作流程、开发流程',
            'data_schema': json.dumps({
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
            }),
            'design_config': json.dumps({
                'template': 'sequence-zigzag-steps-underline-text'
            }),
            'tags': json.dumps(['流程', '步骤', '折线', 'zigzag']),
            'sort_order': 95,
            'is_active': True
        }
        
        template = Template(**template_data)
        db.add(template)
        db.commit()
        print(f'✅ 模板已添加: {template.id}')
        
    except Exception as e:
        db.rollback()
        print(f'❌ 添加失败: {e}')
    finally:
        db.close()

if __name__ == '__main__':
    add_template()
