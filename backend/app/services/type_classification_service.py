"""
类型识别服务
用于识别用户文本的内容类型（7大分类）
"""
import json
import logging
from typing import Dict, Any
from app.services.llm_client import get_llm_client
from app.utils.prompt_manager import get_prompt_manager

logger = logging.getLogger(__name__)


class TypeClassificationService:
    """类型识别服务类"""
    
    def __init__(self):
        """初始化服务"""
        self.llm_client = get_llm_client()
        self.prompt_manager = get_prompt_manager()
    
    async def classify(self, user_text: str) -> Dict[str, Any]:
        """
        识别用户文本的内容类型
        
        Args:
            user_text: 用户输入的文本
        
        Returns:
            Dict: {
                "type": "sequence",
                "confidence": 0.95,
                "reason": "文本包含明确的步骤顺序和流程描述"
            }
        
        Raises:
            Exception: 识别失败时抛出异常
        """
        try:
            logger.info(f"[TypeClassification] 开始识别内容类型 - 文本长度: {len(user_text)}")
            
            # 特殊处理：检测SWOT分析内容
            swot_result = self._detect_swot_content(user_text)
            if swot_result:
                logger.info(f"[TypeClassification] 检测到SWOT内容，直接返回comparison类型")
                return swot_result
            
            # 获取提示词
            system_prompt, user_prompt, temperature, model = \
                self.prompt_manager.get_type_classification_prompt(user_text)
            
            logger.info(f"[TypeClassification] system_prompt长度: {len(system_prompt)}, "
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
            
            logger.info(f"[TypeClassification] LLM原始响应: {response[:200]}...")
            
            # 解析JSON响应
            result = self._parse_response(response)
            
            # 验证结果
            self._validate_result(result)
            
            logger.info(f"[TypeClassification] 识别成功 - 类型: {result['type']}, "
                       f"置信度: {result['confidence']}")
            
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"[TypeClassification] JSON解析失败: {e}, 原始响应: {response}")
            raise Exception("AI返回格式错误，请重试")
        except Exception as e:
            logger.error(f"[TypeClassification] 识别失败: {e}")
            raise
    
    def _detect_swot_content(self, user_text: str) -> Dict[str, Any]:
        """
        检测文本是否为SWOT分析内容
        
        Args:
            user_text: 用户输入的文本
        
        Returns:
            Dict: 如果是SWOT内容，返回classification结果；否则返回None
        """
        import re
        
        # 转换为小写进行匹配
        text_lower = user_text.lower()
        
        # SWOT关键词匹配
        swot_keywords = [
            'swot',
            'strengths',
            'weaknesses', 
            'opportunities',
            'threats',
            '优势',
            '劣势',
            '机会',
            '威胁'
        ]
        
        # 计算匹配到的关键词数量
        matched_count = sum(1 for keyword in swot_keywords if keyword in text_lower)
        
        # 如果匹配到3个或以上SWOT相关关键词，认为是SWOT分析
        if matched_count >= 3:
            return {
                "type": "comparison",
                "confidence": 0.98,
                "reason": f"文本包含SWOT分析的关键要素（匹配{matched_count}个关键词），属于对比型内容，应使用SWOT分析模板展示优势、劣势、机会、威胁四个维度的对比分析。"
            }
        
        return None
    
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
    
    def _validate_result(self, result: Dict[str, Any]):
        """
        验证识别结果
        
        Args:
            result: 识别结果
        
        Raises:
            ValueError: 结果格式不正确时抛出
        """
        # 检查必需字段
        required_fields = ['type', 'confidence', 'reason']
        for field in required_fields:
            if field not in result:
                raise ValueError(f"识别结果缺少必需字段: {field}")
        
        # 验证类型值
        valid_types = ['chart', 'comparison', 'hierarchy', 'list', 'quadrant', 'relationship', 'sequence']
        if result['type'] not in valid_types:
            logger.warning(f"[TypeClassification] 未知类型: {result['type']}，使用list作为默认值")
            result['type'] = 'list'
        
        # 验证置信度
        if not isinstance(result['confidence'], (int, float)) or not (0 <= result['confidence'] <= 1):
            logger.warning(f"[TypeClassification] 置信度异常: {result['confidence']}，设置为0.5")
            result['confidence'] = 0.5
        
        # 验证理由
        if not isinstance(result['reason'], str) or not result['reason']:
            result['reason'] = "未提供理由"


# 全局服务实例
_type_classification_service = None


def get_type_classification_service() -> TypeClassificationService:
    """获取类型识别服务单例"""
    global _type_classification_service
    if _type_classification_service is None:
        _type_classification_service = TypeClassificationService()
    return _type_classification_service
