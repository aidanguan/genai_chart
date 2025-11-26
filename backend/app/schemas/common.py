"""
通用Schema定义
"""
from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, Any

T = TypeVar('T')


class APIResponse(BaseModel, Generic[T]):
    """统一API响应格式"""
    success: bool
    data: Optional[T] = None
    message: str = "操作成功"


class ErrorResponse(BaseModel):
    """错误响应格式"""
    success: bool = False
    error: dict
