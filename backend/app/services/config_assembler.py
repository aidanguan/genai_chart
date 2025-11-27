"""
配置拼接器
将Dify返回的data与模板的design_config拼接成完整的配置对象
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class ConfigAssembler:
    """配置拼接器"""
    
    def assemble_config(
        self,
        data: Dict[str, Any],
        design_config: Dict[str, Any],
        template_id: str
    ) -> Dict[str, Any]:
        """
        拼接完整的AntV Infographic配置对象
        
        Args:
            data: 业务数据（来自Dify工作流）
            design_config: 设计配置（来自模板表）
            template_id: 模板ID（用于日志）
        
        Returns:
            Dict: 完整的配置对象 {
                "data": {...},    # 业务数据
                "design": {...},  # 设计配置
                "theme": {...},   # 主题配置
                "layout": {...}   # 布局配置
            }
        """
        logger.info(f"[ConfigAssembler] 开始拼接配置 - 模板: {template_id}")
        
        # 提取design配置
        design = design_config.get('design', {})
        
        # 构建完整配置
        config = {
            "data": data,
            "design": design,
            # 使用默认主题和布局
            "theme": self._get_default_theme(),
            "layout": self._get_default_layout()
        }
        
        logger.info(f"[ConfigAssembler] 配置拼接完成 - 模板: {template_id}")
        
        return config
    
    def _get_default_theme(self) -> Dict[str, Any]:
        """
        获取默认主题配置
        
        Returns:
            Dict: 主题配置对象
        """
        return {
            "name": "default",
            "colors": {
                "palette": [
                    "#5B8FF9",
                    "#5AD8A6",
                    "#5D7092",
                    "#F6BD16",
                    "#E86452",
                    "#6DC8EC",
                    "#945FB9",
                    "#FF9845",
                    "#1E9493",
                    "#FF99C3"
                ]
            }
        }
    
    def _get_default_layout(self) -> Dict[str, Any]:
        """
        获取默认布局配置
        
        Returns:
            Dict: 布局配置对象
        """
        return {
            "width": 800,
            "height": 600,
            "padding": [20, 20, 20, 20]
        }


# 单例模式
_config_assembler = None


def get_config_assembler() -> ConfigAssembler:
    """获取配置拼接器单例"""
    global _config_assembler
    if _config_assembler is None:
        _config_assembler = ConfigAssembler()
    return _config_assembler
