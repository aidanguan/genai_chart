#!/usr/bin/env python3
"""
修复 compare-binary-horizontal 模板的 designConfig
"""
import sys
import os
import json

# 添加父目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.utils.db import get_db_session
from app.repositories.template_repo import TemplateRepository
from sqlalchemy import text

def fix_compare_binary_horizontal():
    """修复 compare-binary-horizontal 的 designConfig"""
    db = get_db_session()
    
    try:
        # 正确的 designConfig (基于 AntV Infographic 内置模板)
        correct_design_config = {
            "design": {
                "structure": {
                    "type": "compare-binary-horizontal",
                    "dividerType": "vs"
                },
                "title": "default",
                "items": [{"type": "simple", "iconType": "circle", "iconSize": 40}]
            }
        }
        
        print("=" * 60)
        print("修复 compare-binary-horizontal 模板")
        print("=" * 60)
        
        # 更新模板
        result = db.execute(
            text("""
                UPDATE templates 
                SET design_config = :design_config,
                    structure_type = :structure_type
                WHERE id = :template_id
            """),
            {
                "design_config": json.dumps(correct_design_config),
                "structure_type": "compare-binary-horizontal",
                "template_id": "compare-binary-horizontal"
            }
        )
        
        db.commit()
        
        print(f"✅ 已更新 compare-binary-horizontal 模板")
        print(f"   - 设置正确的 designConfig")
        print(f"   - structure_type: compare-binary-horizontal")
        print(f"   - design.structure.type: compare-binary-horizontal")
        print(f"   - design.items: [{{\"type\": \"simple\", \"iconType\": \"circle\", \"iconSize\": 40}}]")
        print(f"   - dividerType: vs")
        
        # 验证更新结果
        repo = TemplateRepository(db)
        template = repo.get_by_id("compare-binary-horizontal")
        if template:
            print("\n验证更新结果:")
            print(json.dumps(template.to_dict()["designConfig"], indent=2, ensure_ascii=False))
        
        print("\n✅ 修复完成!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    fix_compare_binary_horizontal()
