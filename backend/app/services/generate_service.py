"""
生成服务
处理信息图生成相关逻辑
"""
import logging
import time
from typing import Dict, Any
from app.services.llm_client import get_llm_client
from app.services.template_service import get_template_service

logger = logging.getLogger(__name__)


class GenerateService:
    """生成服务类"""
    
    def __init__(self):
        """初始化生成服务"""
        self.llm_client = get_llm_client()
        self.template_service = get_template_service()
    
    async def recommend_templates(
        self,
        user_text: str,
        max_recommendations: int = 5
    ) -> Dict[str, Any]:
        """
        推荐模板
        
        Args:
            user_text: 用户输入的文本
            max_recommendations: 最多推荐数量
        
        Returns:
            Dict: 包含推荐结果和分析时间
        """
        start_time = time.time()
        
        # 获取所有可用模板
        result = self.template_service.get_all_templates(page=1, page_size=100)
        available_templates = result.get("templates", [])
        
        # 调用LLM推荐
        recommendations = await self.llm_client.recommend_templates(
            user_text=user_text,
            available_templates=available_templates,
            max_recommendations=max_recommendations
        )
        
        analysis_time = round(time.time() - start_time, 2)
        
        return {
            "recommendations": recommendations,
            "analysisTime": analysis_time
        }
    
    async def extract_data(
        self,
        user_text: str,
        template_id: str
    ) -> Dict[str, Any]:
        """
        提取结构化数据
        
        Args:
            user_text: 用户输入的文本
            template_id: 模板ID
        
        Returns:
            Dict: 包含配置对象和提取时间
        """
        start_time = time.time()
        
        # 获取模板信息
        template = self.template_service.get_template_by_id(template_id)
        if not template:
            raise ValueError(f"模板ID不存在: {template_id}")
        
        # 获取模板Schema
        template_schema = template.get("dataSchema", {})
        
        # 调用LLM提取数据
        extracted_data = await self.llm_client.extract_structured_data(
            user_text=user_text,
            template_id=template_id,
            template_schema=template_schema
        )
        
        # 获取AntV模板配置映射
        from app.services.template_service import TEMPLATE_DESIGN_MAP
        template_design = TEMPLATE_DESIGN_MAP.get(template_id, {})
        
        # 构建完整的AntV Infographic配置
        config = {
            **template_design,
            "data": extracted_data.get("data", {}),
            "themeConfig": extracted_data.get("themeConfig", {"palette": "antv"})
        }
        
        extraction_time = round(time.time() - start_time, 2)
        
        return {
            "config": config,
            "extractionTime": extraction_time
        }


# 全局生成服务实例
_generate_service = None


def get_generate_service() -> GenerateService:
    """获取生成服务单例"""
    global _generate_service
    if _generate_service is None:
        _generate_service = GenerateService()
    return _generate_service
