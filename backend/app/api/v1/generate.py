"""
生成相关API端点
"""
from fastapi import APIRouter, HTTPException
from app.schemas.common import APIResponse
from app.schemas.infographic import DataExtractRequest, DataExtractResponse
from app.services.generate_service import get_generate_service

router = APIRouter()


@router.post("/extract", summary="提取结构化数据")
async def extract_data(request: DataExtractRequest):
    """
    从用户文本中提取结构化数据，生成信息图配置
    
    - **text**: 用户输入的文本内容
    - **templateId**: 使用的模板ID
    """
    try:
        generate_service = get_generate_service()
        result = await generate_service.extract_data(
            user_text=request.text,
            template_id=request.templateId
        )
        
        return APIResponse(
            success=True,
            data=result,
            message="数据提取成功"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
