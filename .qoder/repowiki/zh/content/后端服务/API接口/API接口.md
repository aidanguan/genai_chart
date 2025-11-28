# API接口

<cite>
**本文档中引用的文件**  
- [export.py](file://backend/app/api/v1/export.py)
- [generate.py](file://backend/app/api/v1/generate.py)
- [templates.py](file://backend/app/api/v1/templates.py)
- [works.py](file://backend/app/api/v1/works.py)
- [main.py](file://backend/app/main.py)
- [common.py](file://backend/app/schemas/common.py)
- [export_service.py](file://backend/app/services/export_service.py)
- [template_service.py](file://backend/app/services/template_service.py)
- [config.py](file://backend/app/config.py)
- [export.ts](file://frontend/src/api/export.ts)
- [generate.ts](file://frontend/src/api/generate.ts)
- [templates.ts](file://frontend/src/api/templates.ts)
- [work.ts](file://frontend/src/api/work.ts)
</cite>

## 目录
1. [API概览](#api概览)
2. [API版本控制与基础信息](#api版本控制与基础信息)
3. [认证机制与安全性](#认证机制与安全性)
4. [跨域资源共享（CORS）配置](#跨域资源共享（cors）配置)
5. [统一响应格式](#统一响应格式)
6. [输入验证与异常处理](#输入验证与异常处理)
7. [核心API端点详解](#核心api端点详解)
   1. [导出端点 (/export)](#导出端点-export)
   2. [生成端点 (/generate)](#生成端点-generate)
   3. [模板端点 (/templates)](#模板端点-templates)
   4. [作品端点 (/works)](#作品端点-works)
8. [API使用示例](#api使用示例)
9. [速率限制](#速率限制)
10. [附录：错误码定义](#附录：错误码定义)

## API概览

本API接口文档详细描述了基于FastAPI实现的四个核心端点：`export`、`generate`、`templates`和`works`。这些端点构成了AI信息图生成系统的核心功能，支持从模板管理、智能生成、作品保存到多格式导出的完整工作流。

系统采用RESTful设计风格，所有API均通过JSON格式进行请求和响应。API遵循统一的响应格式，确保客户端能够一致地处理成功和错误情况。后端服务通过`main.py`文件中的FastAPI应用实例进行路由注册，每个功能模块都有独立的API路由器。

**API端点映射**
```mermaid
graph TD
A[API根路径 /api/v1] --> B[/export]
A --> C[/generate]
A --> D[/templates]
A --> E[/works]
B --> B1[POST /]
B --> B2[GET /download/{filename}]
B --> B3[DELETE /cleanup/{filename}]
B --> B4[GET /formats]
C --> C1[POST /smart]
C --> C2[POST /extract]
C --> C3[GET /debug/workflow-mapper]
D --> D1[GET /]
D --> D2[GET /categories]
D --> D3[GET /{template_id}]
D --> D4[POST /recommend]
E --> E1[POST /]
E --> E2[GET /]
E --> E3[GET /{work_id}]
```

**Diagram sources**
- [main.py](file://backend/app/main.py#L58-L80)

**Section sources**
- [main.py](file://backend/app/main.py#L1-L113)

## API版本控制与基础信息

本API采用基于URL的版本控制策略，所有端点均位于`/api/v1/`前缀下。这种设计允许未来在不破坏现有客户端的情况下引入新的API版本。

### 基础信息
- **API根路径**: `/api/v1`
- **文档路径**: `/docs` (Swagger UI)
- **健康检查**: `/health`
- **当前版本**: 1.0.0

### 版本控制策略
系统采用语义化版本控制（Semantic Versioning），版本号格式为`MAJOR.MINOR.PATCH`：
- **MAJOR**: 当进行不兼容的API更改时递增
- **MINOR**: 当以向后兼容的方式添加功能时递增
- **PATCH**: 当进行向后兼容的错误修复时递增

版本信息通过`main.py`中的`app`实例配置，并在根路径和健康检查端点中返回。

```python
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="基于AntV Infographic的AI信息图生成系统后端API"
)
```

**Section sources**
- [main.py](file://backend/app/main.py#L22-L26)
- [config.py](file://backend/app/config.py#L21-L22)

## 认证机制与安全性

当前系统采用开放的认证策略，所有API端点均无需身份验证即可访问。这种设计适用于内部系统或开发环境，但在生产环境中应考虑增加认证机制。

### 安全性考虑
1. **无认证**: 所有端点对任何来源开放，适合原型和内部使用
2. **输入验证**: 所有请求数据均通过Pydantic模型进行严格验证
3. **异常处理**: 全局异常处理器防止敏感信息泄露
4. **依赖安全**: 关键操作（如PPTX导出）需要特定的Python包

### 未来增强建议
- 实现JWT（JSON Web Token）认证
- 添加API密钥验证
- 实现OAuth2.0授权
- 增加请求签名机制

**Section sources**
- [main.py](file://backend/app/main.py#L38-L54)
- [config.py](file://backend/app/config.py#L13-L19)

## 跨域资源共享（CORS）配置

系统配置了宽松的CORS（跨域资源共享）策略，允许来自任何来源的请求。这在开发阶段非常有用，但生产环境应限制为特定的可信来源。

### CORS配置详情
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 临时允许所有来源，用于调试
    allow_credentials=False,  # 与allow_origins=["*"]一起使用
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 配置参数说明
- **allow_origins**: 允许的来源列表，`["*"]`表示允许所有来源
- **allow_credentials**: 是否允许携带凭据（如cookies），当`allow_origins`为`["*"]`时必须为`False`
- **allow_methods**: 允许的HTTP方法，`["*"]`表示允许所有方法
- **allow_headers**: 允许的请求头，`["*"]`表示允许所有头

生产环境建议将`allow_origins`设置为具体的前端应用URL，如`["http://localhost:5173", "https://yourdomain.com"]`。

**Section sources**
- [main.py](file://backend/app/main.py#L28-L36)
- [config.py](file://backend/app/config.py#L25-L27)

## 统一响应格式

所有API端点遵循统一的响应格式，确保客户端能够一致地处理响应。成功响应和错误响应都包含`success`标志，便于快速判断请求结果。

### 成功响应格式
```json
{
  "success": true,
  "data": { /* 响应数据 */ },
  "message": "操作成功"
}
```

### 错误响应格式
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "错误描述",
    "details": "详细信息（仅在DEBUG模式下显示）"
  }
}
```

### 响应模型定义
```python
class APIResponse(BaseModel, Generic[T]):
    """统一API响应格式"""
    success: bool
    data: Optional[T] = None
    message: str = "操作成功"
```

这种统一格式简化了客户端的错误处理逻辑，开发者只需检查`success`字段即可确定请求是否成功。

**Section sources**
- [common.py](file://backend/app/schemas/common.py#L10-L14)
- [main.py](file://backend/app/main.py#L40-L54)

## 输入验证与异常处理

系统采用多层次的输入验证和异常处理机制，确保API的健壮性和安全性。

### 输入验证
所有请求数据均通过Pydantic模型进行验证，包括：
- **类型检查**: 确保数据类型正确
- **必填字段**: 使用`...`表示必填字段
- **字段约束**: 使用`Field`定义描述、默认值和验证规则
- **嵌套验证**: 支持复杂的数据结构验证

### 异常处理
系统实现了分层的异常处理策略：
1. **全局异常处理器**: 捕获未处理的异常，返回统一的错误响应
2. **端点级异常处理**: 针对特定错误返回有意义的错误信息
3. **服务级异常处理**: 业务逻辑中的异常被捕获并转换为API响应

```python
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "服务器内部错误",
                "details": str(exc) if settings.DEBUG_MODE else None
            }
        }
    )
```

**Section sources**
- [common.py](file://backend/app/schemas/common.py#L10-L20)
- [main.py](file://backend/app/main.py#L39-L54)
- [export.py](file://backend/app/api/v1/export.py#L108-L121)

## 核心API端点详解

### 导出端点 (/export)

导出端点提供将信息图配置渲染为SVG并导出为多种格式的功能。

#### 端点列表
| HTTP方法 | URL路径 | 功能 |
|---------|--------|------|
| POST | /export | 导出信息图为指定格式 |
| GET | /export/download/{filename} | 下载导出的文件 |
| DELETE | /export/cleanup/{filename} | 清理临时文件 |
| GET | /export/formats | 获取支持的导出格式 |

#### POST /export - 导出信息图
**请求参数**
```json
{
  "svgContent": "SVG内容字符串",
  "format": "svg/png/pdf/pptx",
  "filename": "可选的文件名",
  "title": "标题(仅PPTX)",
  "width": 800,
  "height": 600,
  "scale": 2
}
```

**请求体结构**
- `svgContent` (string, 必填): SVG内容字符串
- `format` (string, 必填): 导出格式
- `filename` (string, 可选): 文件名
- `title` (string, 可选): PPTX文件的标题
- `width` (integer, 可选): PNG图像的宽度
- `height` (integer, 可选): PNG图像的高度
- `scale` (integer, 可选): PNG图像的缩放比例

**响应格式**
```json
{
  "success": true,
  "data": {
    "format": "导出格式",
    "filename": "文件名",
    "filepath": "文件路径",
    "size": "文件大小(字节)",
    "downloadUrl": "下载URL",
    "width": "图像宽度(仅PNG)",
    "height": "图像高度(仅PNG)"
  },
  "message": "操作成功"
}
```

**成功示例**
```json
{
  "success": true,
  "data": {
    "format": "png",
    "filename": "infographic.png",
    "filepath": "temp/exports/infographic.png",
    "size": 12345,
    "downloadUrl": "/api/v1/export/download/infographic.png",
    "width": 1600,
    "height": 1200
  },
  "message": "操作成功"
}
```

**错误示例**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "不支持的导出格式: jpg",
    "details": null
  }
}
```

**Section sources**
- [export.py](file://backend/app/api/v1/export.py#L38-L106)

#### GET /export/formats - 获取支持的导出格式
返回所有支持的导出格式及其详细信息。

**响应示例**
```json
{
  "success": true,
  "data": [
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
  ],
  "message": "获取支持的导出格式成功"
}
```

**Section sources**
- [export.py](file://backend/app/api/v1/export.py#L175-L207)

### 生成端点 (/generate)

生成端点提供智能生成信息图的功能，支持两种模式：智能生成和传统模式。

#### 端点列表
| HTTP方法 | URL路径 | 功能 |
|---------|--------|------|
| POST | /generate/smart | 智能生成信息图（三阶段流程） |
| POST | /generate/extract | 提取结构化数据（传统模式） |
| GET | /generate/debug/workflow-mapper | 查看WorkflowMapper调试信息 |

#### POST /generate/smart - 智能生成信息图
**请求参数**
```json
{
  "text": "用户输入的文本内容"
}
```

**请求体结构**
- `text` (string, 必填): 用户输入的文本内容

**响应格式**
```json
{
  "success": true,
  "data": {
    "config": "AntV Infographic配置对象",
    "classification": "类型识别结果",
    "selection": "模板选择结果",
    "timing": "各阶段耗时统计"
  },
  "message": "智能生成成功"
}
```

**成功示例**
```json
{
  "success": true,
  "data": {
    "config": {
      "type": "list-row-horizontal-icon-arrow",
      "data": [
        {"label": "步骤一", "desc": "描述内容"},
        {"label": "步骤二", "desc": "描述内容"}
      ]
    },
    "classification": {
      "type": "流程图",
      "confidence": 0.95,
      "reason": "文本包含多个步骤和顺序关系"
    },
    "selection": {
      "templateId": "list-row-horizontal-icon-arrow",
      "templateName": "图标横向流程图",
      "confidence": 0.9,
      "reason": "最适合展示线性流程"
    },
    "timing": {
      "classification": 120,
      "selection": 80,
      "extraction": 150
    }
  },
  "message": "智能生成成功"
}
```

**Section sources**
- [generate.py](file://backend/app/api/v1/generate.py#L31-L57)

#### POST /generate/extract - 提取结构化数据
**请求参数**
```json
{
  "text": "用户输入的文本内容",
  "templateId": "使用的模板ID",
  "llmProvider": "LLM提供商"
}
```

**请求体结构**
- `text` (string, 必填): 用户输入的文本内容
- `templateId` (string, 必填): 使用的模板ID
- `llmProvider` (string, 可选): LLM提供商 (system 或 dify)

**响应格式**
```json
{
  "success": true,
  "data": {
    "config": "AntV Infographic配置对象"
  },
  "message": "数据提取成功"
}
```

**Section sources**
- [generate.py](file://backend/app/api/v1/generate.py#L62-L83)

### 模板端点 (/templates)

模板端点提供模板管理功能，包括获取模板列表、分类和推荐。

#### 端点列表
| HTTP方法 | URL路径 | 功能 |
|---------|--------|------|
| GET | /templates | 获取模板列表 |
| GET | /templates/categories | 获取模板分类列表 |
| GET | /templates/{template_id} | 获取模板详情 |
| POST | /templates/recommend | AI推荐模板 |

#### GET /templates - 获取模板列表
**查询参数**
- `category` (string, 可选): 按分类筛选
- `keyword` (string, 可选): 搜索关键词
- `page` (integer, 可选): 页码，默认1
- `pageSize` (integer, 可选): 每页数量，默认20

**响应格式**
```json
{
  "success": true,
  "data": {
    "templates": [
      {
        "id": "模板ID",
        "name": "模板名称",
        "category": "分类",
        "description": "描述",
        "适用场景": "适用场景"
      }
    ],
    "total": "总数",
    "page": "当前页码",
    "pageSize": "每页数量"
  },
  "message": "获取模板列表成功"
}
```

**Section sources**
- [templates.py](file://backend/app/api/v1/templates.py#L17-L39)

#### POST /templates/recommend - AI推荐模板
**请求参数**
```json
{
  "text": "用户输入的文本内容",
  "maxRecommendations": 5
}
```

**请求体结构**
- `text` (string, 必填): 用户输入的文本内容
- `maxRecommendations` (integer, 可选): 最多推荐数量，默认5个

**响应格式**
```json
{
  "success": true,
  "data": {
    "recommendations": [
      {
        "templateId": "模板ID",
        "templateName": "模板名称",
        "confidence": "置信度",
        "reason": "推荐理由",
        "category": "分类"
      }
    ]
  },
  "message": "模板推荐成功"
}
```

**Section sources**
- [templates.py](file://backend/app/api/v1/templates.py#L77-L96)

### 作品端点 (/works)

作品端点提供作品管理功能，包括保存、获取和查看作品。

#### 端点列表
| HTTP方法 | URL路径 | 功能 |
|---------|--------|------|
| POST | /works | 保存作品 |
| GET | /works | 获取作品列表 |
| GET | /works/{work_id} | 获取作品详情 |

#### POST /works - 保存作品
**请求参数**
```json
{
  "title": "作品标题",
  "templateId": "使用的模板ID",
  "inputText": "用户输入的原始文本",
  "infographicConfig": "完整的Infographic配置"
}
```

**请求体结构**
- `title` (string, 可选): 作品标题
- `templateId` (string, 必填): 使用的模板ID
- `inputText` (string, 必填): 用户输入的原始文本
- `infographicConfig` (object, 必填): 完整的Infographic配置

**响应格式**
```json
{
  "success": true,
  "data": {
    "id": "作品ID",
    "title": "作品标题",
    "templateId": "模板ID",
    "inputText": "原始文本",
    "infographicConfig": "配置",
    "createdAt": "创建时间",
    "updatedAt": "更新时间"
  },
  "message": "作品保存成功"
}
```

**Section sources**
- [works.py](file://backend/app/api/v1/works.py#L15-L45)

#### GET /works - 获取作品列表
**查询参数**
- `userId` (string, 可选): 用户ID筛选
- `page` (integer, 可选): 页码，默认1
- `pageSize` (integer, 可选): 每页数量，默认20

**响应格式**
```json
{
  "success": true,
  "data": {
    "works": [
      {
        "id": "作品ID",
        "title": "作品标题",
        "templateId": "模板ID",
        "inputText": "原始文本",
        "infographicConfig": "配置",
        "createdAt": "创建时间",
        "updatedAt": "更新时间"
      }
    ],
    "total": "总数",
    "page": "当前页码",
    "pageSize": "每页数量"
  },
  "message": "获取作品列表成功"
}
```

**Section sources**
- [works.py](file://backend/app/api/v1/works.py#L50-L77)

## API使用示例

### 使用curl调用API

#### 导出信息图为PNG
```bash
curl -X POST "http://localhost:8000/api/v1/export" \
  -H "Content-Type: application/json" \
  -d '{
    "svgContent": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"800\" height=\"600\"></svg>",
    "format": "png",
    "filename": "mychart.png",
    "width": 800,
    "height": 600,
    "scale": 2
  }'
```

#### 智能生成信息图
```bash
curl -X POST "http://localhost:8000/api/v1/generate/smart" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "公司第一季度销售报告显示，产品A销售额为100万，产品B销售额为80万，产品C销售额为120万。"
  }'
```

#### 推荐模板
```bash
curl -X POST "http://localhost:8000/api/v1/templates/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "我需要展示公司组织架构，包括CEO、CTO、CFO和各部门负责人。",
    "maxRecommendations": 3
  }'
```

#### 保存作品
```bash
curl -X POST "http://localhost:8000/api/v1/works" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Q1销售报告",
    "templateId": "bar-chart-vertical",
    "inputText": "产品A销售额为100万，产品B销售额为80万，产品C销售额为120万。",
    "infographicConfig": {
      "type": "bar-chart-vertical",
      "data": [
        {"name": "产品A", "value": 100},
        {"name": "产品B", "value": 80},
        {"name": "产品C", "value": 120}
      ]
    }
  }'
```

### 使用Python requests库

```python
import requests
import json

# 基础URL
BASE_URL = "http://localhost:8000/api/v1"

# 智能生成信息图
def smart_generate(text):
    url = f"{BASE_URL}/generate/smart"
    payload = {"text": text}
    response = requests.post(url, json=payload)
    return response.json()

# 推荐模板
def recommend_templates(text, max_recommendations=5):
    url = f"{BASE_URL}/templates/recommend"
    payload = {
        "text": text,
        "maxRecommendations": max_recommendations
    }
    response = requests.post(url, json=payload)
    return response.json()

# 导出为PNG
def export_to_png(svg_content, filename="chart.png"):
    url = f"{BASE_URL}/export"
    payload = {
        "svgContent": svg_content,
        "format": "png",
        "filename": filename,
        "width": 800,
        "height": 600,
        "scale": 2
    }
    response = requests.post(url, json=payload)
    return response.json()

# 保存作品
def save_work(title, template_id, input_text, config):
    url = f"{BASE_URL}/works"
    payload = {
        "title": title,
        "templateId": template_id,
        "inputText": input_text,
        "infographicConfig": config
    }
    response = requests.post(url, json=payload)
    return response.json()

# 使用示例
if __name__ == "__main__":
    # 智能生成
    result = smart_generate("公司第一季度销售报告显示，产品A销售额为100万，产品B销售额为80万，产品C销售额为120万。")
    print("智能生成结果:", json.dumps(result, indent=2, ensure_ascii=False))
    
    # 推荐模板
    recommendations = recommend_templates("我需要展示公司组织架构", 3)
    print("模板推荐:", json.dumps(recommendations, indent=2, ensure_ascii=False))
    
    # 保存作品
    work_result = save_work(
        "Q1销售报告",
        "bar-chart-vertical",
        "产品A销售额为100万，产品B销售额为80万，产品C销售额为120万。",
        result["data"]["config"]
    )
    print("保存作品:", json.dumps(work_result, indent=2, ensure_ascii=False))
```

**Section sources**
- [export.ts](file://frontend/src/api/export.ts)
- [generate.ts](file://frontend/src/api/generate.ts)
- [templates.ts](file://frontend/src/api/templates.ts)
- [work.ts](file://frontend/src/api/work.ts)

## 速率限制

当前系统未实现速率限制机制。所有客户端可以无限制地调用API端点。

### 建议的速率限制策略
1. **基于IP的限制**: 对每个IP地址设置请求频率限制
2. **基于令牌的限制**: 使用API密钥进行配额管理
3. **分层限制**: 对不同端点设置不同的限制策略

例如，可以使用`slowapi`库实现速率限制：
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/generate/smart")
@limiter.limit("5/minute")
async def smart_generate(request: SmartGenerateRequest):
    # 端点逻辑
    pass
```

**Section sources**
- [main.py](file://backend/app/main.py#L1-L113)

## 附录：错误码定义

| 错误码 | HTTP状态码 | 描述 |
|-------|-----------|------|
| INTERNAL_ERROR | 500 | 服务器内部错误 |
| VALIDATION_ERROR | 400 | 请求数据验证失败 |
| NOT_FOUND | 404 | 资源未找到 |
| UNAUTHORIZED | 401 | 未授权访问 |
| RATE_LIMIT_EXCEEDED | 429 | 请求频率超过限制 |

**Section sources**
- [main.py](file://backend/app/main.py#L40-L54)
- [export.py](file://backend/app/api/v1/export.py#L108-L121)