"""
检查数据库中模板的实际配置
"""
import sys
import os
import json

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.db import get_db
from app.models.template import Template


def check_template():
    """检查模板配置"""
    
    with get_db() as db:
        template = db.query(Template).filter(Template.id == 'bar-chart-vertical').first()
        
        if not template:
            print("❌ 未找到模板")
            return
        
        print(f"模板ID: {template.id}")
        print(f"模板名称: {template.name}")
        print(f"\n原始 design_config (从数据库):")
        print(json.dumps(template.design_config, ensure_ascii=False, indent=2))
        
        print(f"\n转换后的 designConfig (通过to_dict()):")
        template_dict = template.to_dict()
        print(json.dumps(template_dict.get('designConfig'), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    check_template()
