"""
作品管理API端点
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.schemas.common import APIResponse
from app.schemas.work import WorkCreateRequest, WorkResponse
from app.utils.db import get_db_session
from app.repositories.work_repo import WorkRepository
from app.models.work import UserWork

router = APIRouter()


@router.post("", summary="保存作品")
async def create_work(request: WorkCreateRequest):
    """
    保存用户创建的信息图作品
    
    - **title**: 作品标题(可选)
    - **templateId**: 使用的模板ID
    - **inputText**: 用户输入的原始文本
    - **infographicConfig**: 完整的Infographic配置
    """
    db = get_db_session()
    try:
        repo = WorkRepository(db)
        
        # 创建作品对象
        work = UserWork(
            title=request.title,
            template_id=request.templateId,
            input_text=request.inputText,
            infographic_config=request.infographicConfig,
            user_id=request.userId  # 可选,后期扩展
        )
        
        # 保存到数据库
        created_work = repo.create(work)
        
        return APIResponse(
            success=True,
            data=created_work.to_dict(),
            message="作品保存成功"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"保存作品失败: {str(e)}")
    finally:
        db.close()


@router.get("", summary="获取作品列表")
async def get_works(
    userId: Optional[str] = Query(None, description="用户ID筛选"),
    page: int = Query(1, description="页码", ge=1),
    pageSize: int = Query(20, description="每页数量", ge=1, le=100)
):
    """
    获取作品列表(分页)
    
    - **userId**: 用户ID(可选,用于筛选特定用户的作品)
    - **page**: 页码(默认1)
    - **pageSize**: 每页数量(默认20)
    """
    db = get_db_session()
    try:
        repo = WorkRepository(db)
        works, total = repo.get_all(user_id=userId, page=page, page_size=pageSize)
        
        return APIResponse(
            success=True,
            data={
                "works": [w.to_dict() for w in works],
                "total": total,
                "page": page,
                "pageSize": pageSize
            },
            message="获取作品列表成功"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取作品列表失败: {str(e)}")
    finally:
        db.close()


@router.get("/{work_id}", summary="获取作品详情")
async def get_work_detail(work_id: int):
    """
    获取指定作品的详细信息
    
    - **work_id**: 作品ID
    """
    db = get_db_session()
    try:
        repo = WorkRepository(db)
        work = repo.get_by_id(work_id)
        
        if not work:
            raise HTTPException(status_code=404, detail=f"作品不存在: {work_id}")
        
        return APIResponse(
            success=True,
            data=work.to_dict(),
            message="获取作品详情成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取作品详情失败: {str(e)}")
    finally:
        db.close()
