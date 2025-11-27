"""
数据校验器
验证Dify返回的数据是否符合模板的schema定义
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class DataValidator:
    """数据校验器"""
    
    def validate_against_schema(
        self,
        data: Dict[str, Any],
        schema: Dict[str, Any],
        template_id: str
    ) -> Dict[str, Any]:
        """
        根据schema校验数据，并尝试修复问题
        
        Args:
            data: 需要校验的数据
            schema: 模板的数据schema定义
            template_id: 模板ID（用于日志）
        
        Returns:
            Dict: {
                "valid": bool,  # 是否通过校验
                "data": dict,   # 校验后的数据（可能已修复）
                "errors": list  # 错误列表
            }
        """
        logger.info(f"[DataValidator] 开始校验数据 - 模板: {template_id}")
        
        errors = []
        validated_data = data.copy()
        
        # 获取dataFields定义
        data_fields = schema.get('dataFields', {})
        
        # 校验每个字段
        for field_name, field_def in data_fields.items():
            field_type = field_def.get('type')
            required = field_def.get('required', False)
            
            # 检查必填字段
            if required and field_name not in validated_data:
                errors.append(f"缺少必填字段: {field_name}")
                continue
            
            # 如果字段不存在且非必填，跳过
            if field_name not in validated_data:
                continue
            
            field_value = validated_data[field_name]
            
            # 类型校验
            if field_type == 'string':
                if not isinstance(field_value, str):
                    errors.append(f"字段{field_name}类型错误，期望string，实际{type(field_value).__name__}")
            
            elif field_type == 'number':
                if not isinstance(field_value, (int, float)):
                    # 尝试转换
                    try:
                        validated_data[field_name] = float(field_value)
                        logger.info(f"[DataValidator] 字段{field_name}已转换为number")
                    except:
                        errors.append(f"字段{field_name}无法转换为number")
            
            elif field_type == 'array':
                if not isinstance(field_value, list):
                    errors.append(f"字段{field_name}类型错误，期望array，实际{type(field_value).__name__}")
                else:
                    # 校验数组项
                    item_schema = field_def.get('itemSchema', {})
                    validated_items = []
                    
                    for idx, item in enumerate(field_value):
                        item_errors = self._validate_item(item, item_schema, f"{field_name}[{idx}]")
                        if item_errors:
                            errors.extend(item_errors)
                        else:
                            validated_items.append(item)
                    
                    validated_data[field_name] = validated_items
        
        # 判断是否通过校验
        valid = len(errors) == 0
        
        if valid:
            logger.info(f"[DataValidator] 校验通过 - 模板: {template_id}")
        else:
            logger.warning(f"[DataValidator] 校验失败 - 模板: {template_id}, 错误: {errors}")
        
        return {
            "valid": valid,
            "data": validated_data,
            "errors": errors
        }
    
    def _validate_item(
        self,
        item: Any,
        item_schema: Dict[str, Any],
        path: str
    ) -> List[str]:
        """
        校验数组项
        
        Args:
            item: 数组项
            item_schema: 项的schema定义
            path: 当前路径（用于错误信息）
        
        Returns:
            List[str]: 错误列表
        """
        errors = []
        
        if not isinstance(item, dict):
            errors.append(f"{path}应为对象类型")
            return errors
        
        # 校验每个字段
        for field_name, field_def in item_schema.items():
            field_type = field_def.get('type')
            required = field_def.get('required', False)
            
            if required and field_name not in item:
                errors.append(f"{path}.{field_name}缺少必填字段")
                continue
            
            if field_name not in item:
                continue
            
            field_value = item[field_name]
            
            # 类型校验
            if field_type == 'string' and not isinstance(field_value, str):
                errors.append(f"{path}.{field_name}类型错误，期望string")
            elif field_type == 'number' and not isinstance(field_value, (int, float)):
                errors.append(f"{path}.{field_name}类型错误，期望number")
        
        return errors


# 单例模式
_data_validator = None


def get_data_validator() -> DataValidator:
    """获取数据校验器单例"""
    global _data_validator
    if _data_validator is None:
        _data_validator = DataValidator()
    return _data_validator
