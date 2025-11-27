"""
导出API接口
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional
import os

from app.services.export_service import get_export_service, SUPPORTED_FORMATS
from app.schemas.common import APIResponse

router = APIRouter(tags=["导出"])


class ExportRequest(BaseModel):
    """导出请求"""
    svgContent: str = Field(..., description="SVG内容")
    format: str = Field(..., description="导出格式: svg/png/pdf/pptx")
    filename: Optional[str] = Field(None, description="文件名")
    title: Optional[str] = Field("信息图", description="标题(仅PPTX)")
    width: Optional[int] = Field(800, description="宽度(仅PNG)")
    height: Optional[int] = Field(600, description="高度(仅PNG)")
    scale: Optional[int] = Field(2, description="缩放比例(仅PNG)")


class ExportResponse(BaseModel):
    """导出响应"""
    format: str
    filename: str
    filepath: str
    size: int
    downloadUrl: str
    width: Optional[int] = None
    height: Optional[int] = None


@router.post("", summary="导出信息图", response_model=APIResponse[ExportResponse])
async def export_infographic(request: ExportRequest):
    """
    导出信息图为指定格式
    
    - **svgContent**: SVG内容字符串
    - **format**: 导出格式 (svg/png/pdf/pptx)
    - **filename**: 可选的文件名
    - **title**: 标题(仅用于PPTX格式)
    - **width**: 宽度(仅用于PNG格式)
    - **height**: 高度(仅用于PNG格式)
    - **scale**: 缩放比例(仅用于PNG格式)
    """
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"开始导出, 格式: {request.format}, SVG长度: {len(request.svgContent)}")
        
        export_service = get_export_service()
        
        # 验证格式
        if request.format not in SUPPORTED_FORMATS:
            error_msg = f"不支持的导出格式: {request.format}"
            logger.error(error_msg)
            return APIResponse(
                success=False,
                error=error_msg
            )
        
        # 准备导出参数
        export_kwargs = {
            "filename": request.filename
        }
        
        if request.format == "png":
            export_kwargs.update({
                "width": request.width,
                "height": request.height,
                "scale": request.scale
            })
        elif request.format == "pptx":
            export_kwargs["title"] = request.title
        
        logger.info(f"导出参数: {export_kwargs}")
        
        # 执行导出
        result = export_service.export(
            svg_content=request.svgContent,
            format=request.format,
            **export_kwargs
        )
        
        logger.info(f"导出成功: {result}")
        
        # 构建下载URL
        download_url = f"/api/v1/export/download/{result['filename']}"
        
        response_data = ExportResponse(
            format=result["format"],
            filename=result["filename"],
            filepath=result["filepath"],
            size=result["size"],
            downloadUrl=download_url,
            width=result.get("width"),
            height=result.get("height")
        )
        
        return APIResponse(success=True, data=response_data)
        
    except ImportError as e:
        error_msg = f"缺少必要的依赖库: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return APIResponse(
            success=False,
            error=error_msg
        )
    except Exception as e:
        error_msg = f"导出失败: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return APIResponse(
            success=False,
            error=error_msg
        )


@router.get("/download/{filename}", summary="下载导出文件")
async def download_file(filename: str):
    """
    下载导出的文件
    
    - **filename**: 文件名
    """
    export_service = get_export_service()
    filepath = export_service.temp_dir / filename
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="文件不存在")
    
    # 根据扩展名设置媒体类型
    media_types = {
        ".svg": "image/svg+xml",
        ".png": "image/png",
        ".pdf": "application/pdf",
        ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    }
    
    ext = os.path.splitext(filename)[1].lower()
    media_type = media_types.get(ext, "application/octet-stream")
    
    return FileResponse(
        path=str(filepath),
        filename=filename,
        media_type=media_type
    )


@router.delete("/cleanup/{filename}", summary="清理临时文件")
async def cleanup_file(filename: str):
    """
    清理临时导出文件
    
    - **filename**: 文件名
    """
    try:
        export_service = get_export_service()
        filepath = str(export_service.temp_dir / filename)
        export_service.cleanup(filepath)
        
        return APIResponse(success=True, message="文件已清理")
    except Exception as e:
        return APIResponse(
            success=False,
            error=f"清理失败: {str(e)}"
        )


@router.get("/formats", summary="获取支持的导出格式")
async def get_formats():
    """
    获取所有支持的导出格式列表
    """
    formats = [
        {
            "value": "svg",
            "label": "SVG",
            "description": "矢量图形格式，可无限缩放",
            "extension": ".svg"
        },
        {
            "value": "png",
            "label": "PNG",
            "description": "高质量位图格式",
            "extension": ".png"
        },
        {
            "value": "pdf",
            "label": "PDF",
            "description": "便携式文档格式",
            "extension": ".pdf"
        },
        {
            "value": "pptx",
            "label": "PPTX",
            "description": "PowerPoint演示文稿",
            "extension": ".pptx"
        }
    ]
    
    return APIResponse(success=True, data=formats)
