"""
模板相关Schema定义
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class TemplateRecommendRequest(BaseModel):
    """模板推荐请求"""
    text: str = Field(..., description="用户输入的文本内容", min_length=1)
    maxRecommendations: int = Field(5, description="最多推荐数量", ge=1, le=10)


class TemplateRecommendation(BaseModel):
    """单个模板推荐结果"""
    templateId: str
    templateName: str
    confidence: float
    reason: str
    category: Optional[str] = None


class TemplateRecommendResponse(BaseModel):
    """模板推荐响应"""
    recommendations: List[TemplateRecommendation]
    analysisTime: float
