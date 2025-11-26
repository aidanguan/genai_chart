"""
模板数据导入脚本
从JSON文件导入模板数据到数据库
"""
import sys
import os
import json
import logging
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.db import get_db
from app.models.template import Template

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def validate_template(template_data: dict) -> tuple[bool, str]:
    """
    验证模板数据完整性
    
    Args:
        template_data: 模板数据字典
    
    Returns:
        (是否有效, 错误信息)
    """
    required_fields = ['id', 'name', 'category', 'data_schema', 'design_config']
    
    for field in required_fields:
        if field not in template_data:
            return False, f"缺少必填字段: {field}"
    
    # 验证分类是否有效
    valid_categories = ['chart', 'comparison', 'hierarchy', 'list', 'quadrant', 'relation', 'sequence']
    if template_data['category'] not in valid_categories:
        return False, f"无效的分类: {template_data['category']}"
    
    return True, ""


def import_templates(json_file: str, skip_existing: bool = True):
    """
    导入模板数据
    
    Args:
        json_file: JSON文件路径
        skip_existing: 是否跳过已存在的模板
    """
    # 读取JSON文件
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            templates_data = json.load(f)
    except Exception as e:
        logger.error(f"读取JSON文件失败: {e}")
        return
    
    logger.info(f"从 {json_file} 读取到 {len(templates_data)} 个模板")
    
    # 统计
    success_count = 0
    skip_count = 0
    error_count = 0
    errors = []
    
    with get_db() as db:
        for idx, template_data in enumerate(templates_data, 1):
            template_id = template_data.get('id', f'unknown_{idx}')
            
            try:
                # 验证数据
                is_valid, error_msg = validate_template(template_data)
                if not is_valid:
                    error_count += 1
                    errors.append(f"{template_id}: {error_msg}")
                    logger.warning(f"[{idx}/{len(templates_data)}] ⚠️  {template_id} - {error_msg}")
                    continue
                
                # 检查是否已存在
                existing = db.query(Template).filter(Template.id == template_id).first()
                if existing and skip_existing:
                    skip_count += 1
                    logger.info(f"[{idx}/{len(templates_data)}] ⏭️  {template_id} - 已存在,跳过")
                    continue
                
                # 创建或更新模板
                if existing:
                    # 更新
                    existing.name = template_data['name']
                    existing.category = template_data['category']
                    existing.description = template_data.get('description')
                    existing.use_cases = template_data.get('use_cases')
                    existing.preview_url = template_data.get('preview_url')
                    existing.data_schema = template_data['data_schema']
                    existing.design_config = template_data['design_config']
                    existing.tags = template_data.get('tags')
                    existing.sort_order = template_data.get('sort_order', 0)
                    existing.is_active = template_data.get('is_active', True)
                    existing.updated_at = datetime.utcnow()
                    logger.info(f"[{idx}/{len(templates_data)}] 🔄 {template_id} - 更新成功")
                else:
                    # 新增
                    template = Template(
                        id=template_id,
                        name=template_data['name'],
                        category=template_data['category'],
                        description=template_data.get('description'),
                        use_cases=template_data.get('use_cases'),
                        preview_url=template_data.get('preview_url'),
                        data_schema=template_data['data_schema'],
                        design_config=template_data['design_config'],
                        tags=template_data.get('tags'),
                        sort_order=template_data.get('sort_order', 0),
                        is_active=template_data.get('is_active', True)
                    )
                    db.add(template)
                    logger.info(f"[{idx}/{len(templates_data)}] ✅ {template_id} - 导入成功")
                
                success_count += 1
                
            except Exception as e:
                error_count += 1
                errors.append(f"{template_id}: {str(e)}")
                logger.error(f"[{idx}/{len(templates_data)}] ❌ {template_id} - 导入失败: {e}")
    
    # 打印导入报告
    logger.info("\n" + "="*60)
    logger.info("导入报告")
    logger.info("="*60)
    logger.info(f"总数: {len(templates_data)}")
    logger.info(f"成功: {success_count}")
    logger.info(f"跳过: {skip_count}")
    logger.info(f"失败: {error_count}")
    
    if errors:
        logger.info("\n错误详情:")
        for error in errors:
            logger.error(f"  - {error}")
    
    logger.info("="*60)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='导入模板数据到数据库')
    parser.add_argument('json_file', help='模板JSON文件路径')
    parser.add_argument('--force', action='store_true', help='强制更新已存在的模板')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.json_file):
        logger.error(f"文件不存在: {args.json_file}")
        sys.exit(1)
    
    import_templates(args.json_file, skip_existing=not args.force)


if __name__ == "__main__":
    main()
