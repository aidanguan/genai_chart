"""
模板选择服务
用于从指定类型的模板中选择最合适的一个
"""
import json
import logging
from typing import Dict, Any, List
from app.services.llm_client import get_llm_client
from app.utils.prompt_manager import get_prompt_manager
from app.services.template_service import get_template_service

logger = logging.getLogger(__name__)


class TemplateSelectionService:
    """模板选择服务类"""
    
    def __init__(self):
        """初始化服务"""
        self.llm_client = get_llm_client()
        self.prompt_manager = get_prompt_manager()
        self.template_service = get_template_service()
    
    async def select(self, user_text: str, content_type: str) -> Dict[str, Any]:
        """
        从指定类型的模板中选择最合适的一个
        
        Args:
            user_text: 用户输入的文本
            content_type: 内容类型 (chart/comparison/hierarchy/list/quadrant/relationship/sequence)
        
        Returns:
            Dict: {
                "templateId": "sequence-timeline-simple",
                "templateName": "简单时间轴",
                "confidence": 0.92,
                "reason": "用户文本描述了按时间顺序的事件，时间轴模板最适合"
            }
        
        Raises:
            Exception: 选择失败时抛出异常
        """
        try:
            logger.info(f"[TemplateSelection] 开始选择模板 - 类型: {content_type}, 文本长度: {len(user_text)}")
            
            # 获取该类型的所有模板
            templates = self.template_service.get_templates_by_category(content_type)
            
            if not templates:
                logger.warning(f"[TemplateSelection] 未找到类型为 {content_type} 的模板，使用所有模板")
                # 如果没有该类型的模板，使用所有模板
                result = self.template_service.get_all_templates(page=1, page_size=100)
                templates = result.get("templates", [])
            
            logger.info(f"[TemplateSelection] 找到 {len(templates)} 个候选模板")
            
            # 获取提示词
            system_prompt, user_prompt, temperature, model = \
                self.prompt_manager.get_template_selection_prompt(user_text, content_type, templates)
            
            logger.info(f"[TemplateSelection] system_prompt长度: {len(system_prompt)}, "
                       f"user_prompt长度: {len(user_prompt)}, temperature: {temperature}")
            
            # 构造消息
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            # 调用LLM
            response = await self.llm_client.chat_completion(
                messages=messages,
                model=model,
                temperature=temperature
            )
            
            logger.info(f"[TemplateSelection] LLM原始响应: {response[:200]}...")
            
            # 解析JSON响应
            result = self._parse_response(response)
            
            # 验证结果
            self._validate_result(result, templates)
            
            logger.info(f"[TemplateSelection] 选择成功 - 模板: {result['templateId']}, "
                       f"置信度: {result['confidence']}")
            
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"[TemplateSelection] JSON解析失败: {e}, 原始响应: {response}")
            raise Exception("AI返回格式错误，请重试")
        except Exception as e:
            logger.error(f"[TemplateSelection] 选择失败: {e}")
            raise
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """
        解析LLM响应
        
        Args:
            response: LLM返回的原始响应
        
        Returns:
            Dict: 解析后的结果
        """
        # 尝试直接解析JSON
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            pass
        
        # 尝试提取JSON（处理可能包含markdown代码块的情况）
        import re
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            return json.loads(json_match.group())
        
        # 无法解析
        raise json.JSONDecodeError("无法解析JSON响应", response, 0)
    
    def _validate_result(self, result: Dict[str, Any], templates: List[Dict[str, Any]]):
        """
        验证选择结果
        
        Args:
            result: 选择结果
            templates: 可选模板列表
        
        Raises:
            ValueError: 结果格式不正确时抛出
        """
        # 检查必需字段
        required_fields = ['templateId', 'templateName', 'confidence', 'reason']
        for field in required_fields:
            if field not in result:
                raise ValueError(f"选择结果缺少必需字段: {field}")
        
        # 验证模板ID是否在候选列表中
        template_ids = [t['id'] for t in templates]
        if result['templateId'] not in template_ids:
            logger.warning(f"[TemplateSelection] 选择的模板ID不在候选列表中: {result['templateId']}")
            # 使用第一个模板作为默认值
            if templates:
                result['templateId'] = templates[0]['id']
                result['templateName'] = templates[0]['name']
                logger.info(f"[TemplateSelection] 使用默认模板: {result['templateId']}")
        
        # 验证置信度
        if not isinstance(result['confidence'], (int, float)) or not (0 <= result['confidence'] <= 1):
            logger.warning(f"[TemplateSelection] 置信度异常: {result['confidence']}，设置为0.5")
            result['confidence'] = 0.5
        
        # 验证理由
        if not isinstance(result['reason'], str) or not result['reason']:
            result['reason'] = "未提供理由"


# 全局服务实例
_template_selection_service = None


def get_template_selection_service() -> TemplateSelectionService:
    """获取模板选择服务单例"""
    global _template_selection_service
    if _template_selection_service is None:
        _template_selection_service = TemplateSelectionService()
    return _template_selection_service
