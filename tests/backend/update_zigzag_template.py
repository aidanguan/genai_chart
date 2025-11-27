"""更新 sequence-zigzag-steps-underline-text 模板配置"""
from app.utils.db import get_db_session
from app.models.template import Template

def update_template():
    db = get_db_session()
    
    try:
        t = db.query(Template).filter(
            Template.id == 'sequence-zigzag-steps-underline-text'
        ).first()
        
        if not t:
            print("❌ 模板不存在")
            return
        
        # 更新为字典格式（SQLAlchemy的JSON列会自动处理）
        t.design_config = {
            'template': 'sequence-zigzag-steps-underline-text'
        }
        
        t.data_schema = {
            'description': 'W型折线步骤图',
            'dataFields': {
                'title': {
                    'type': 'string',
                    'required': False,
                    'description': '标题'
                },
                'desc': {
                    'type': 'string',
                    'required': False,
                    'description': '描述'
                },
                'items': {
                    'type': 'array',
                    'required': True,
                    'description': '步骤列表',
                    'itemSchema': {
                        'label': {
                            'type': 'string',
                            'required': True,
                            'description': '步骤名称'
                        },
                        'desc': {
                            'type': 'string',
                            'required': False,
                            'description': '步骤描述'
                        }
                    }
                }
            }
        }
        
        db.commit()
        print('✅ 模板配置已更新')
        
        # 验证
        db.refresh(t)
        print(f'验证 - design_config类型: {type(t.design_config)}')
        print(f'验证 - design_config内容: {t.design_config}')
        
    except Exception as e:
        db.rollback()
        print(f'❌ 更新失败: {e}')
    finally:
        db.close()

if __name__ == '__main__':
    update_template()
