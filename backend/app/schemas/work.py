"""
作品相关Schema定义
"""
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional


class WorkCreateRequest(BaseModel):
    """作品创建请求"""
    title: Optional[str] = Field(None, description="作品标题")
    templateId: str = Field(..., description="使用的模板ID")
    inputText: str = Field(..., description="用户输入的原始文本", min_length=1)
    infographicConfig: Dict[str, Any] = Field(..., description="完整的Infographic配置")
    userId: Optional[str] = Field(None, description="用户ID(可选)")


class WorkResponse(BaseModel):
    """作品响应"""
    id: int
    title: Optional[str]
    templateId: str
    inputText: str
    infographicConfig: Dict[str, Any]
    thumbnailUrl: Optional[str]
    createdAt: str
    updatedAt: str
