# API集成

<cite>
**本文档引用的文件**
- [client.ts](file://frontend/src/api/client.ts)
- [generate.ts](file://frontend/src/api/generate.ts)
- [templates.ts](file://frontend/src/api/templates.ts)
- [work.ts](file://frontend/src/api/work.ts)
- [export.ts](file://frontend/src/api/export.ts)
- [generate.py](file://backend/app/api/v1/generate.py)
- [templates.py](file://backend/app/api/v1/templates.py)
- [works.py](file://backend/app/api/v1/works.py)
- [export.py](file://backend/app/api/v1/export.py)
- [template.ts](file://frontend/src/stores/template.ts)
- [workspace.ts](file://frontend/src/stores/workspace.ts)
</cite>

## 目录
1. [API客户端封装策略](#api客户端封装策略)
2. [API模块接口定义](#api模块接口定义)
3. [典型调用场景](#典型调用场景)
4. [错误处理与重试机制](#错误处理与重试机制)
5. [类型安全与数据模型映射](#类型安全与数据模型映射)
6. [缓存策略](#缓存策略)

## API客户端封装策略

前端通过axios封装了统一的API客户端，实现了请求拦截、响应处理和错误统一捕获。API客户端配置了120秒的超时时间，以支持Dify工作流的长时间处理。

```mermaid
classDiagram
class APIResponse {
+success : boolean
+data? : T
+message? : string
+error? : string
}
class APIClient {
+baseURL : string
+timeout : number
+headers : object
+interceptors : object
}
APIClient --> APIResponse : "返回"
```

**图示来源**
- [client.ts](file://frontend/src/api/client.ts#L9-L14)

**本节来源**
- [client.ts](file://frontend/src/api/client.ts#L1-L46)

## API模块接口定义

### 生成模块

生成模块提供智能生成和传统模式两种API接口。智能生成采用三阶段流程：类型识别、模板选择和数据提取。

```mermaid
sequenceDiagram
participant 前端 as 前端
participant 生成API as generateAPI
participant 后端 as 后端
前端->>生成API : smartGenerate(text)
生成API->>后端 : POST /generate/smart
后端-->>生成API : 智能生成响应
生成API-->>前端 : 返回配置数据
```

**图示来源**
- [generate.ts](file://frontend/src/api/generate.ts#L7-L25)
- [generate.py](file://backend/app/api/v1/generate.py#L31-L58)

**本节来源**
- [generate.ts](file://frontend/src/api/generate.ts#L7-L25)
- [generate.py](file://backend/app/api/v1/generate.py#L1-L116)

### 模板模块

模板模块提供模板列表获取、分类查询和AI推荐功能。模板数据结构包含ID、名称、分类和描述等字段。

```mermaid
classDiagram
class Template {
+id : string
+name : string
+category : string
+description : string
+适用场景 : string
}
class TemplateRecommendation {
+templateId : string
+templateName : string
+confidence : number
+reason : string
+category? : string
}
class TemplateAPI {
+getTemplates(params) : Promise
+getCategories() : Promise
+recommendTemplates(params) : Promise
}
TemplateAPI --> Template : "返回"
TemplateAPI --> TemplateRecommendation : "返回"
```

**图示来源**
- [templates.ts](file://frontend/src/api/templates.ts#L6-L22)
- [templates.py](file://backend/app/api/v1/templates.py#L17-L40)

**本节来源**
- [templates.ts](file://frontend/src/api/templates.ts#L1-L52)
- [templates.py](file://backend/app/api/v1/templates.py#L1-L99)

### 作品模块

作品模块管理用户创建的信息图作品，支持作品的创建、查询和删除操作。

```mermaid
classDiagram
class WorkCreateRequest {
+title : string
+templateId : string
+inputText : string
+infographicConfig : any
}
class Work {
+id : number
+title : string
+templateId : string
+inputText : string
+infographicConfig : any
+createdAt : string
+updatedAt : string
}
class WorkAPI {
+createWork(data) : Promise
+getWorks(page, pageSize) : Promise
+getWork(id) : Promise
+deleteWork(id) : Promise
}
WorkAPI --> WorkCreateRequest : "接收"
WorkAPI --> Work : "返回"
```

**图示来源**
- [work.ts](file://frontend/src/api/work.ts#L10-L28)
- [works.py](file://backend/app/api/v1/works.py#L16-L48)

**本节来源**
- [work.ts](file://frontend/src/api/work.ts#L1-L62)
- [works.py](file://backend/app/api/v1/works.py#L1-L106)

### 导出模块

导出模块支持将信息图导出为SVG、PNG、PDF和PPTX等多种格式，并提供文件下载和清理功能。

```mermaid
classDiagram
class ExportRequest {
+svgContent : string
+format : 'svg'|'png'|'pdf'|'pptx'
+filename? : string
+title? : string
+width? : number
+height? : number
+scale? : number
}
class ExportResponse {
+format : string
+filename : string
+filepath : string
+size : number
+downloadUrl : string
+width? : number
+height? : number
}
class ExportFormat {
+value : string
+label : string
+description : string
+extension : string
}
class ExportAPI {
+exportInfographic(data) : Promise
+getExportFormats() : Promise
+getDownloadUrl(filename) : string
+cleanupFile(filename) : Promise
}
ExportAPI --> ExportRequest : "接收"
ExportAPI --> ExportResponse : "返回"
ExportAPI --> ExportFormat : "返回"
```

**图示来源**
- [export.ts](file://frontend/src/api/export.ts#L10-L41)
- [export.py](file://backend/app/api/v1/export.py#L16-L36)

**本节来源**
- [export.ts](file://frontend/src/api/export.ts#L1-L74)
- [export.py](file://backend/app/api/v1/export.py#L1-L208)

## 典型调用场景

### 发起AI生成请求

通过智能生成接口，系统自动识别文本类型、选择合适模板并提取结构化数据。

```mermaid
sequenceDiagram
participant 用户 as 用户
participant 工作区 as 工作区Store
participant 生成API as generateAPI
participant 后端 as 后端
用户->>工作区 : 输入文本内容
工作区->>生成API : smartGenerate(text)
生成API->>后端 : POST /generate/smart
后端-->>生成API : 返回配置数据
生成API-->>工作区 : 解析响应
工作区->>工作区 : 更新infographicConfig
工作区-->>用户 : 显示生成结果
```

**图示来源**
- [workspace.ts](file://frontend/src/stores/workspace.ts#L7-L12)
- [generate.ts](file://frontend/src/api/generate.ts#L11-L13)

**本节来源**
- [generate.ts](file://frontend/src/api/generate.ts#L11-L13)
- [workspace.ts](file://frontend/src/stores/workspace.ts#L1-L74)

### 获取模板列表

获取所有可用模板或按分类筛选模板，支持分页查询。

```mermaid
flowchart TD
Start([开始]) --> SetParams["设置查询参数<br/>category, keyword, page, pageSize"]
SetParams --> CallAPI["调用getTemplates API"]
CallAPI --> CheckSuccess{"请求成功?"}
CheckSuccess --> |是| ProcessData["处理返回数据<br/>更新templates数组"]
CheckSuccess --> |否| HandleError["处理错误<br/>显示错误信息"]
ProcessData --> End([结束])
HandleError --> End
```

**图示来源**
- [templates.ts](file://frontend/src/api/templates.ts#L26-L28)
- [template.ts](file://frontend/src/stores/template.ts#L44-L53)

**本节来源**
- [templates.ts](file://frontend/src/api/templates.ts#L26-L28)
- [template.ts](file://frontend/src/stores/template.ts#L36-L102)

### 保存用户作品

将用户创建的信息图作品保存到服务器，包括标题、模板ID、输入文本和配置数据。

```mermaid
sequenceDiagram
participant 前端 as 前端组件
participant 作品API as workAPI
participant 后端 as 后端
前端->>作品API : createWork(data)
作品API->>后端 : POST /works
后端-->>作品API : 返回作品信息
作品API-->>前端 : 解析响应
前端->>前端 : 更新UI状态
```

**图示来源**
- [work.ts](file://frontend/src/api/work.ts#L33-L35)
- [works.py](file://backend/app/api/v1/works.py#L16-L48)

**本节来源**
- [work.ts](file://frontend/src/api/work.ts#L33-L35)
- [works.py](file://backend/app/api/v1/works.py#L16-L48)

## 错误处理与重试机制

API客户端实现了统一的错误处理机制，所有请求失败都会在控制台输出错误信息。后端API返回标准的响应结构，包含success、data、message和error字段。

```mermaid
flowchart TD
Request[发起请求] --> Interceptor["请求拦截器"]
Interceptor --> Send["发送HTTP请求"]
Send --> Response{"收到响应?"}
Response --> |是| Success{"响应成功?"}
Response --> |否| NetworkError["网络错误"]
Success --> |是| ReturnData["返回data字段"]
Success --> |否| HandleError["处理业务错误"]
NetworkError --> LogError["记录错误日志"]
HandleError --> LogError
LogError --> ThrowError["抛出错误"]
ThrowError --> Catch["调用方捕获"]
```

**图示来源**
- [client.ts](file://frontend/src/api/client.ts#L36-L45)
- [generate.py](file://backend/app/api/v1/generate.py#L58-L59)

**本节来源**
- [client.ts](file://frontend/src/api/client.ts#L36-L45)
- [generate.py](file://backend/app/api/v1/generate.py#L58-L59)

## 类型安全与数据模型映射

前端使用TypeScript定义了与后端数据模型对应的接口类型，确保类型安全的前后端通信。API响应结构统一，便于类型推断和错误处理。

```mermaid
classDiagram
class APIResponse {
+success : boolean
+data? : T
+message? : string
+error? : string
}
class BackendModel {
+id : number
+title : string
+template_id : string
+input_text : string
+infographic_config : object
+created_at : datetime
+updated_at : datetime
}
class FrontendModel {
+id : number
+title : string
+templateId : string
+inputText : string
+infographicConfig : any
+createdAt : string
+updatedAt : string
}
APIResponse <|-- WorkResponse
BackendModel <--> FrontendModel : "数据映射"
WorkResponse --> FrontendModel : "类型约束"
```

**图示来源**
- [work.ts](file://frontend/src/api/work.ts#L5-L28)
- [works.py](file://backend/app/api/v1/works.py#L7-L10)

**本节来源**
- [work.ts](file://frontend/src/api/work.ts#L5-L28)
- [works.py](file://backend/app/api/v1/works.py#L7-L10)

## 缓存策略

系统通过Pinia状态管理实现了模板数据的客户端缓存，减少重复API调用。模板列表和分类信息在首次获取后存储在store中，后续访问直接从内存读取。

```mermaid
flowchart LR
User[用户请求] --> CheckCache{"缓存中存在?"}
CheckCache --> |是| ReturnFromCache["从缓存返回数据"]
CheckCache --> |否| FetchFromAPI["调用API获取数据"]
FetchFromAPI --> UpdateCache["更新缓存"]
UpdateCache --> ReturnData["返回数据"]
ReturnFromCache --> End
ReturnData --> End
```

**图示来源**
- [template.ts](file://frontend/src/stores/template.ts#L38-L41)
- [template.ts](file://frontend/src/stores/template.ts#L44-L53)

**本节来源**
- [template.ts](file://frontend/src/stores/template.ts#L36-L102)