"""
工作流映射管理器
管理模板ID到Dify工作流的映射关系
"""
import os
import logging
from typing import Dict, Any, Optional
import yaml

logger = logging.getLogger(__name__)


class WorkflowMapper:
    """工作流映射管理器"""
    
    def __init__(self):
        """初始化映射管理器"""
        self.config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'config',
            'dify_workflows.yaml'
        )
        logger.info(f"[WorkflowMapper.__init__] 初始化，配置文件路径: {self.config_path}")
        self.mappings = self._load_config()
        logger.info(f"[WorkflowMapper.__init__] 加载完成，映射数量: {len(self.mappings)}, 模板列表: {list(self.mappings.keys())}")
    
    def _load_config(self) -> Dict[str, Any]:
        """
        加载工作流映射配置
        
        Returns:
            Dict: 映射配置字典
        """
        try:
            if not os.path.exists(self.config_path):
                logger.warning(f"[WorkflowMapper] 配置文件不存在: {self.config_path}")
                return {}
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f) or {}
            
            logger.info(f"[WorkflowMapper] 成功加载配置，共{len(config)}个模板映射")
            return config
            
        except Exception as e:
            logger.error(f"[WorkflowMapper] 加载配置失败: {e}")
            return {}
    
    def get_workflow_config(self, template_id: str) -> Optional[Dict[str, Any]]:
        """
        获取模板的工作流配置
        
        Args:
            template_id: 模板ID
        
        Returns:
            Dict: 工作流配置，如果不存在或未启用则返回None
                {
                    "dify_app_id": str or None,
                    "workflow_name": str,
                    "enabled": bool,
                    "fallback_to_system_llm": bool
                }
        """
        config = self.mappings.get(template_id)
        
        if not config:
            logger.debug(f"[WorkflowMapper] 模板{template_id}无工作流配置")
            return None
        
        if not config.get('enabled', False):
            logger.debug(f"[WorkflowMapper] 模板{template_id}的工作流未启用")
            return None
        
        return config
    
    def is_workflow_enabled(self, template_id: str) -> bool:
        """
        检查模板是否启用了工作流
        
        Args:
            template_id: 模板ID
        
        Returns:
            bool: 是否启用工作流
        """
        config = self.get_workflow_config(template_id)
        return config is not None
    
    def should_fallback_to_llm(self, template_id: str) -> bool:
        """
        检查失败时是否应回退到系统LLM
        
        Args:
            template_id: 模板ID
        
        Returns:
            bool: 是否启用回退（默认True）
        """
        config = self.get_workflow_config(template_id)
        if not config:
            return True
        
        return config.get('fallback_to_system_llm', True)
    
    def get_workflow_name(self, template_id: str) -> str:
        """
        获取工作流名称（用于日志）
        
        Args:
            template_id: 模板ID
        
        Returns:
            str: 工作流名称
        """
        config = self.get_workflow_config(template_id)
        if not config:
            return f"未配置的工作流({template_id})"
        
        return config.get('workflow_name', template_id)
    
    def get_app_id(self, template_id: str) -> Optional[str]:
        """
        获取Dify应用ID
        
        Args:
            template_id: 模板ID
        
        Returns:
            str: Dify应用ID，如果为null则返回None（使用默认key）
        """
        config = self.get_workflow_config(template_id)
        if not config:
            return None
        
        return config.get('dify_app_id')
    
    def reload_config(self):
        """重新加载配置（用于热更新）"""
        self.mappings = self._load_config()
        logger.info("[WorkflowMapper] 配置已重新加载")


# 单例模式
_workflow_mapper = None


def get_workflow_mapper() -> WorkflowMapper:
    """获取工作流映射管理器单例"""
    global _workflow_mapper
    if _workflow_mapper is None:
        logger.info("[get_workflow_mapper] 创建新的WorkflowMapper单例")
        _workflow_mapper = WorkflowMapper()
    else:
        logger.debug("[get_workflow_mapper] 返回已存在的WorkflowMapper单例")
    return _workflow_mapper
