"""
生成相关API端点
支持两种模式：
1. 智能生成模式（三阶段：类型识别、模板选择、数据提取）
2. 传统模式（直接指定模板ID进行数据提取）
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.common import APIResponse
from app.schemas.infographic import DataExtractRequest, DataExtractResponse
from app.services.generate_service import get_generate_service
from app.services.workflow_mapper import get_workflow_mapper

router = APIRouter()


class SmartGenerateRequest(BaseModel):
    """智能生成请求"""
    text: str = Field(..., description="用户输入的文本内容")
    includeAllTemplates: bool = Field(
        default=False,
        description="是否返回所有模板列表（带相似度排序）"
    )


class SmartGenerateResponse(BaseModel):
    """智能生成响应"""
    config: dict = Field(..., description="AntV Infographic配置对象")
    classification: dict = Field(..., description="类型识别结果")
    selection: dict = Field(..., description="模板选择结果")
    timing: dict = Field(..., description="各阶段耗时统计")


@router.post("/smart", summary="智能生成信息图（三阶段流程）")
async def smart_generate(request: SmartGenerateRequest):
    """
    智能生成流程，自动识别类型、选择模板、提取数据
    
    流程：
    1. 类型识别：根据文本内容识别合适的图表类型
    2. 模板选择：从该类型的模板中选择最合适的一个
    3. 数据提取：根据模板的数据结构提取关键信息
    
    - **text**: 用户输入的文本内容
    
    返回：
    - **config**: 可直接用于渲染的AntV Infographic配置
    - **classification**: 类型识别结果（type, confidence, reason）
    - **selection**: 模板选择结果（templateId, templateName, confidence, reason）
    - **timing**: 各阶段耗时统计
    """
    try:
        generate_service = get_generate_service()
        result = await generate_service.generate_smart(
            user_text=request.text,
            include_all_templates=request.includeAllTemplates
        )
        
        return APIResponse(
            success=True,
            data=result,
            message="智能生成成功"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract", summary="提取结构化数据（传统模式）")
async def extract_data(request: DataExtractRequest):
    """
    从用户文本中提取结构化数据，生成信息图配置
    
    - **text**: 用户输入的文本内容
    - **templateId**: 使用的模板ID
    - **llmProvider**: LLM提供商 (system 或 dify)，默认system
    """
    try:
        generate_service = get_generate_service()
        result = await generate_service.extract_data(
            user_text=request.text,
            template_id=request.templateId,
            force_provider=request.llmProvider,
            include_all_templates=request.includeAllTemplates
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


@router.get("/debug/workflow-mapper", summary="查看WorkflowMapper调试信息")
async def debug_workflow_mapper():
    """调试端点：查看WorkflowMapper的状态"""
    mapper = get_workflow_mapper()
    
    test_template_ids = ['bar-chart-vertical', 'list-row-horizontal-icon-arrow', 'chart-column-simple']
    
    debug_info = {
        "config_path": mapper.config_path,
        "total_mappings": len(mapper.mappings),
        "all_template_ids": list(mapper.mappings.keys()),
        "test_results": {}
    }
    
    for template_id in test_template_ids:
        debug_info["test_results"][template_id] = {
            "is_workflow_enabled": mapper.is_workflow_enabled(template_id),
            "config": mapper.get_workflow_config(template_id),
            "workflow_name": mapper.get_workflow_name(template_id)
        }
    
    return APIResponse(
        success=True,
        data=debug_info,
        message="WorkflowMapper调试信息"
    )
