"""
信息图相关Schema定义
"""
from pydantic import BaseModel, Field
from typing import Any, Dict


class DataExtractRequest(BaseModel):
    """数据提取请求"""
    text: str = Field(..., description="用户输入的文本内容", min_length=1)
    templateId: str = Field(..., description="模板ID")


class DataExtractResponse(BaseModel):
    """数据提取响应"""
    config: Dict[str, Any]
    extractionTime: float
