"""
LLM客户端服务
封装与AiHubMix API的通信
"""
import json
import logging
from typing import List, Dict, Any, Optional
from openai import OpenAI, APIError, APITimeoutError, RateLimitError
from app.config import get_settings

logger = logging.getLogger(__name__)


class LLMClient:
    """LLM客户端类"""
    
    def __init__(self):
        """初始化LLM客户端"""
        settings = get_settings()
        logger.info(f"[LLMClient] 初始化 - API Key: {settings.AIHUBMIX_API_KEY[:25]}..., Base URL: {settings.AIHUBMIX_BASE_URL}, Model: {settings.AIHUBMIX_MODEL_RECOMMEND}")
        self.client = OpenAI(
            api_key=settings.AIHUBMIX_API_KEY,
            base_url=settings.AIHUBMIX_BASE_URL,
            timeout=settings.AIHUBMIX_TIMEOUT,
            max_retries=settings.AIHUBMIX_MAX_RETRIES
        )
        self.recommend_model = settings.AIHUBMIX_MODEL_RECOMMEND
        self.extract_model = settings.AIHUBMIX_MODEL_EXTRACT
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        response_format: Optional[Dict[str, str]] = None,
        reasoning_effort: str = "medium"
    ) -> str:
        """
        通用聊天补全方法
        
        Args:
            messages: 消息列表
            model: 模型名称，默认使用recommend模型
            temperature: 温度参数
            response_format: 响应格式，例如 {"type": "json_object"}
            reasoning_effort: 推理强度，支持 none, low, medium, high（默认medium）
        
        Returns:
            str: LLM响应内容
        
        Raises:
            Exception: API调用失败时抛出异常
        """
        try:
            if model is None:
                model = self.recommend_model
            
            kwargs = {
                "model": model,
                "messages": messages,
                "temperature": temperature
            }
            
            # 只有 o1/o3 系列推理模型支持reasoning_effort参数
            # gpt-5.1 和其他模型都不支持此参数
            if "o1" in model or "o3" in model:
                kwargs["reasoning_effort"] = reasoning_effort
                # o1/o3 推理模型不支持response_format，必须通过prompt引导JSON输出
            elif response_format:
                # 其他模型添加response_format
                kwargs["response_format"] = response_format
            
            logger.info(f"准备调用LLM: model={model}, kwargs keys={list(kwargs.keys())}")
            response = self.client.chat.completions.create(**kwargs)
            content = response.choices[0].message.content
            
            logger.info(f"LLM调用成功，模型: {model}, tokens使用: {response.usage.total_tokens if response.usage else 'N/A'}")
            
            return content
            
        except APITimeoutError as e:
            logger.error(f"LLM API请求超时: {e}")
            raise Exception("AI服务请求超时，请稍后重试")
        except RateLimitError as e:
            logger.error(f"LLM API配额超限: {e}")
            raise Exception("AI服务配额已用完，请联系管理员")
        except APIError as e:
            logger.error(f"LLM API调用失败: {e}")
            raise Exception(f"AI服务调用失败: {str(e)}")
        except Exception as e:
            logger.error(f"LLM客户端未知错误: {e}")
            raise Exception(f"AI服务发生错误: {str(e)}")
    
    async def recommend_templates(
        self,
        user_text: str,
        available_templates: List[Dict[str, Any]],
        max_recommendations: int = 5
    ) -> List[Dict[str, Any]]:
        """
        推荐信息图模板
        
        Args:
            user_text: 用户输入的文本
            available_templates: 可用模板列表
            max_recommendations: 最多推荐数量
        
        Returns:
            List[Dict]: 推荐模板列表
        """
        from app.utils.prompts import get_template_recommend_prompt
        
        try:
            prompt = get_template_recommend_prompt(user_text, available_templates, max_recommendations)
            
            logger.info(f"[recommend_templates] 开始推荐 - 用户文本长度: {len(user_text)}, 可用模板数: {len(available_templates)}, 最大推荐数: {max_recommendations}")
            logger.info(f"[recommend_templates] 使用模型: {self.recommend_model}")
            
            messages = [
                {"role": "system", "content": "你是一位专业的信息图设计专家，擅长根据文本内容推荐最合适的可视化模板。"},
                {"role": "user", "content": prompt}
            ]
            
            # 根据模型类型决定是否使用response_format
            kwargs = {
                "messages": messages,
                "model": self.recommend_model,
                "temperature": 0.3
            }
            
            # 只有 o1/o3 系列推理模型不支持response_format
            # 其他模型(包括 gpt-5.1)使用response_format来确保JSON输出
            if "o1" not in self.recommend_model and "o3" not in self.recommend_model:
                kwargs["response_format"] = {"type": "json_object"}
                logger.info(f"[recommend_templates] 使用response_format=json_object")
            else:
                logger.info(f"[recommend_templates] o1/o3推理模型，不使用response_format")
            
            logger.info(f"[recommend_templates] 调用LLM，kwargs: {list(kwargs.keys())}")
            response = await self.chat_completion(**kwargs)
            
            result = json.loads(response)
            recommendations = result.get("recommendations", [])
            
            logger.info(f"模板推荐成功，返回{len(recommendations)}个推荐")
            return recommendations
            
        except json.JSONDecodeError as e:
            logger.error(f"解析LLM返回的JSON失败: {e}, 原始响应: {response}")
            raise Exception("AI返回格式错误，请重试")
        except Exception as e:
            logger.error(f"模板推荐失败: {e}")
            raise
    
    async def extract_structured_data(
        self,
        user_text: str,
        template_id: str,
        template_schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        从文本中提取结构化数据
        
        Args:
            user_text: 用户输入的文本
            template_id: 模板ID
            template_schema: 模板数据结构定义
        
        Returns:
            Dict: 结构化的配置数据
        """
        from app.utils.prompts import get_data_extract_prompt
        
        try:
            prompt = get_data_extract_prompt(user_text, template_id, template_schema)
            
            messages = [
                {"role": "system", "content": "你是一位专业的数据分析师，擅长从文本中提取关键信息并转换为结构化数据。"},
                {"role": "user", "content": prompt}
            ]
            
            # 根据模型类型决定是否使用response_format
            kwargs = {
                "messages": messages,
                "model": self.extract_model,
                "temperature": 0.2
            }
            
            # 只有 o1/o3 系列推理模型不支持response_format
            # 其他模型(包括 gpt-5.1)使用response_format来确保JSON输出
            if "o1" not in self.extract_model and "o3" not in self.extract_model:
                kwargs["response_format"] = {"type": "json_object"}
            
            response = await self.chat_completion(**kwargs)
            
            result = json.loads(response)
            
            logger.info(f"数据提取成功，模板: {template_id}")
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"解析LLM返回的JSON失败: {e}, 原始响应: {response}")
            raise Exception("AI返回格式错误，请重试")
        except Exception as e:
            logger.error(f"数据提取失败: {e}")
            raise


# 全局LLM客户端实例
_llm_client: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    """获取LLM客户端单例 - 每次都重新创建以确保加载最新配置"""
    # 暂时禁用单例模式，每次都重新创建以加载最新.env配置
    return LLMClient()
