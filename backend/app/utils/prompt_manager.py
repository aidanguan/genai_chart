"""
提示词管理器
用于加载和管理LLM提示词配置
"""
import os
import yaml
import logging
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class PromptManager:
    """提示词管理器类"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化提示词管理器
        
        Args:
            config_path: 配置文件路径，默认为app/config/llm_prompts.yaml
        """
        if config_path is None:
            # 默认配置文件路径
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "config",
                "llm_prompts.yaml"
            )
        
        self.config_path = config_path
        self.config = {}
        self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        try:
            config_file = Path(self.config_path)
            if not config_file.exists():
                logger.warning(f"配置文件不存在: {self.config_path}，使用默认配置")
                self.config = self._get_default_config()
                return
            
            with open(config_file, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
            
            logger.info(f"成功加载提示词配置: {self.config_path}")
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}，使用默认配置")
            self.config = self._get_default_config()
    
    def reload_config(self):
        """重新加载配置文件"""
        logger.info("重新加载提示词配置...")
        self.load_config()
    
    def get_type_classification_prompt(self, user_text: str) -> tuple[str, str, float, Optional[str]]:
        """
        获取类型识别提示词
        
        Args:
            user_text: 用户输入的文本
        
        Returns:
            tuple: (system_prompt, user_prompt, temperature, model)
        """
        config = self.config.get('type_classification', {})
        
        # 从环境变量获取配置（优先级更高）
        system_prompt = os.getenv('LLM_TYPE_CLASSIFICATION_SYSTEM_PROMPT') or config.get('system_prompt', '')
        user_prompt_template = config.get('user_prompt_template', '')
        temperature = float(os.getenv('LLM_TYPE_CLASSIFICATION_TEMPERATURE', config.get('temperature', 0.3)))
        model = config.get('model')
        
        # 渲染用户提示词模板
        user_prompt = user_prompt_template.format(user_text=user_text)
        
        return system_prompt, user_prompt, temperature, model
    
    def get_template_selection_prompt(
        self,
        user_text: str,
        content_type: str,
        templates: list[Dict[str, Any]]
    ) -> tuple[str, str, float, Optional[str]]:
        """
        获取模板选择提示词
        
        Args:
            user_text: 用户输入的文本
            content_type: 已识别的内容类型
            templates: 模板列表
        
        Returns:
            tuple: (system_prompt, user_prompt, temperature, model)
        """
        config = self.config.get('template_selection', {})
        
        # 从环境变量获取配置（优先级更高）
        system_prompt = os.getenv('LLM_TEMPLATE_SELECTION_SYSTEM_PROMPT') or config.get('system_prompt', '')
        user_prompt_template = config.get('user_prompt_template', '')
        temperature = float(os.getenv('LLM_TEMPLATE_SELECTION_TEMPERATURE', config.get('temperature', 0.3)))
        model = config.get('model')
        
        # 格式化模板列表
        templates_list = self._format_templates_list(templates)
        
        # 渲染用户提示词模板
        user_prompt = user_prompt_template.format(
            user_text=user_text,
            content_type=content_type,
            templates_list=templates_list
        )
        
        return system_prompt, user_prompt, temperature, model
    
    def get_data_extraction_prompt(
        self,
        user_text: str,
        template_id: str,
        schema: Dict[str, Any]
    ) -> tuple[str, str, float, Optional[str]]:
        """
        获取数据提取提示词
        
        Args:
            user_text: 用户输入的文本
            template_id: 模板ID
            schema: 数据结构Schema
        
        Returns:
            tuple: (system_prompt, user_prompt, temperature, model)
        """
        config = self.config.get('data_extraction', {})
        
        # 从环境变量获取配置（优先级更高）
        system_prompt = os.getenv('LLM_DATA_EXTRACTION_SYSTEM_PROMPT') or config.get('system_prompt', '')
        user_prompt_template = config.get('user_prompt_template', '')
        temperature = float(os.getenv('LLM_DATA_EXTRACTION_TEMPERATURE', config.get('temperature', 0.2)))
        model = config.get('model')
        
        # 格式化Schema
        import json
        schema_str = json.dumps(schema, ensure_ascii=False, indent=2)
        
        # 渲染用户提示词模板
        user_prompt = user_prompt_template.format(
            user_text=user_text,
            template_id=template_id,
            schema=schema_str
        )
        
        return system_prompt, user_prompt, temperature, model
    
    def _format_templates_list(self, templates: list[Dict[str, Any]]) -> str:
        """
        格式化模板列表为字符串
        
        Args:
            templates: 模板列表
        
        Returns:
            str: 格式化的模板列表文本
        """
        formatted_list = []
        for tmpl in templates:
            desc = f"""- ID: {tmpl['id']}
  名称: {tmpl.get('name', '未命名')}
  分类: {tmpl.get('category', '未分类')}
  描述: {tmpl.get('description', '暂无描述')}
  适用场景: {tmpl.get('适用场景', tmpl.get('usageScenarios', ''))}"""
            formatted_list.append(desc)
        
        return "\n\n".join(formatted_list)
    
    def _get_default_config(self) -> Dict[str, Any]:
        """
        获取默认配置（如果配置文件不存在）
        
        Returns:
            Dict: 默认配置
        """
        return {
            'type_classification': {
                'system_prompt': '你是一位专业的信息图分类专家，擅长识别文本内容的结构类型。',
                'user_prompt_template': '请分析文本: {user_text}',
                'temperature': 0.3,
                'model': None
            },
            'template_selection': {
                'system_prompt': '你是一位专业的信息图设计专家。',
                'user_prompt_template': '文本: {user_text}\n类型: {content_type}\n模板: {templates_list}',
                'temperature': 0.3,
                'model': None
            },
            'data_extraction': {
                'system_prompt': '你是一位专业的数据分析师。',
                'user_prompt_template': '文本: {user_text}\n模板: {template_id}\nSchema: {schema}',
                'temperature': 0.2,
                'model': None
            }
        }


# 全局PromptManager实例
_prompt_manager: Optional[PromptManager] = None


def get_prompt_manager() -> PromptManager:
    """获取PromptManager单例"""
    global _prompt_manager
    if _prompt_manager is None:
        _prompt_manager = PromptManager()
    return _prompt_manager
