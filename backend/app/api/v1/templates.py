"""
模板相关API端点
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.schemas.common import APIResponse
from app.schemas.template import (
    TemplateRecommendRequest,
    TemplateRecommendResponse
)
from app.services.template_service import get_template_service
from app.services.generate_service import get_generate_service

router = APIRouter()


@router.get("", summary="获取模板列表")
async def get_templates(
    category: Optional[str] = Query(None, description="按分类筛选"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    page: int = Query(1, description="页码", ge=1),
    pageSize: int = Query(20, description="每页数量", ge=1, le=100)
):
    """
    获取可用的信息图模板列表(分页)
    
    - **category**: 模板分类（可选）
    - **keyword**: 搜索关键词（可选）
    - **page**: 页码（默认1）
    - **pageSize**: 每页数量（默认20）
    """
    template_service = get_template_service()
    result = template_service.get_all_templates(
        category=category,
        keyword=keyword,
        page=page,
        page_size=pageSize
    )
    return APIResponse(success=True, data=result, message="获取模板列表成功")


@router.get("/categories", summary="获取模板分类列表")
async def get_categories():
    """
    获取所有模板分类及每个分类的模板数量统计
    
    返回7大分类:
    - 图表型: 数值展示
    - 对比型: 优劣对比
    - 层级型: 组织架构
    - 列表型: 步骤说明
    - 四象限型: 市场定位
    - 关系型: 关系网络
    - 顺序型: 时间线流程
    """
    template_service = get_template_service()
    categories = template_service.get_categories()
    return APIResponse(success=True, data=categories, message="获取分类列表成功")


@router.get("/{template_id}", summary="获取模板详情")
async def get_template_detail(template_id: str):
    """
    获取指定模板的详细信息
    
    - **template_id**: 模板ID
    """
    template_service = get_template_service()
    template = template_service.get_template_by_id(template_id)
    
    if not template:
        raise HTTPException(status_code=404, detail=f"模板不存在: {template_id}")
    
    return APIResponse(success=True, data=template, message="获取模板详情成功")


@router.post("/recommend", summary="AI推荐模板")
async def recommend_templates(request: TemplateRecommendRequest):
    """
    根据用户输入的文本内容，使用AI推荐最合适的信息图模板
    
    - **text**: 用户输入的文本内容
    - **maxRecommendations**: 最多推荐数量（默认5个）
    """
    try:
        generate_service = get_generate_service()
        result = await generate_service.recommend_templates(
            user_text=request.text,
            max_recommendations=request.maxRecommendations
        )
        
        return APIResponse(
            success=True,
            data=result,
            message="模板推荐成功"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
