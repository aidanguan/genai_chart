# 基于AntV Infographic的AI信息图生成系统设计文档

## 一、系统概述

### 1.1 系统定位
本系统是一个基于AntV Infographic组件库的智能信息图生成Web应用,通过集成大语言模型能力,实现从文本内容到可视化信息图的自动化转换。系统为用户提供便捷的信息图创建、编辑、导出和管理功能。

### 1.2 核心价值
- 降低信息图设计门槛,用户无需专业设计技能即可生成高质量信息图
- 通过AI智能分析文本内容,自动推荐合适的图表模板和数据结构
- 支持多种导出格式,满足不同场景的使用需求
- 提供完整的信息图生成和管理生命周期支持

### 1.3 技术栈选型
| 层级 | 技术选型 | 说明 |
|------|---------|------|
| 前端框架 | Vue 3 | 采用Composition API,提供响应式UI交互 |
| 后端框架 | Python FastAPI | 高性能异步框架,支持自动API文档生成 |
| 可视化引擎 | AntV Infographic v0.1.0 | 声明式信息图渲染框架 |
| AI服务提供商 | AiHubMix | 统一的LLM API接口平台 |
| 配置管理 | .env文件 | 环境变量管理,支持灵活配置切换 |

## 二、系统架构设计

### 2.1 整体架构

系统采用前后端分离的三层架构:

```mermaid
graph TB
    subgraph 前端层[前端展示层 - Vue3]
        A[用户界面组件]
        B[状态管理]
        C[AntV Infographic渲染引擎]
    end
    
    subgraph 后端层[后端服务层 - FastAPI]
        D[API网关]
        E[业务逻辑层]
        F[AI处理服务]
    end
    
    subgraph 外部服务层[外部服务层]
        G[AiHubMix LLM服务]
        H[文件存储服务]
    end
    
    A --> D
    B --> D
    C --> A
    D --> E
    E --> F
    F --> G
    E --> H
```

### 2.2 前端架构

前端采用Vue 3框架,基于组件化设计原则:

```mermaid
graph LR
    subgraph 页面层
        A[信息图创建页面]
        B[信息图管理页面]
        C[导出页面]
    end
    
    subgraph 组件层
        D[文本输入组件]
        E[模板选择组件]
        F[样式配置组件]
        G[预览组件]
        H[导出选项组件]
    end
    
    subgraph 服务层
        I[API服务]
        J[状态管理服务]
        K[本地存储服务]
    end
    
    A --> D
    A --> E
    A --> F
    A --> G
    B --> H
    D --> I
    E --> I
    F --> I
    G --> C
    H --> I
    I --> J
    J --> K
```

### 2.3 后端架构

后端基于FastAPI框架,采用分层设计:

```mermaid
graph TB
    subgraph API层
        A[REST API端点]
    end
    
    subgraph 服务层
        B[模板推荐服务]
        C[数据结构化服务]
        D[信息图生成服务]
        E[导出服务]
        F[存储管理服务]
    end
    
    subgraph 集成层
        G[LLM客户端]
        H[文件系统接口]
    end
    
    A --> B
    A --> C
    A --> D
    A --> E
    A --> F
    B --> G
    C --> G
    D --> C
    E --> D
    F --> H
```

## 三、核心功能设计

### 3.1 文本转信息图生成流程

这是系统的核心功能,完整流程如下:

```mermaid
sequenceDiagram
    participant U as 用户
    participant FE as 前端
    participant BE as 后端服务
    participant LLM as LLM服务
    participant IG as Infographic引擎

    U->>FE: 输入文本内容
    FE->>BE: 发送文本内容
    
    rect rgb(200, 220, 240)
        Note over BE,LLM: 阶段1: 模板推荐
        BE->>LLM: 分析文本内容并推荐模板
        LLM-->>BE: 返回推荐模板列表
    end
    
    BE-->>FE: 返回推荐模板
    FE->>U: 展示模板选项
    U->>FE: 确认选择模板
    
    FE->>BE: 提交模板选择
    
    rect rgb(220, 240, 200)
        Note over BE,LLM: 阶段2: 数据结构化
        BE->>LLM: 根据模板要求结构化文本
        LLM-->>BE: 返回结构化数据
    end
    
    BE-->>FE: 返回配置数据
    FE->>IG: 传递配置数据
    IG-->>FE: 生成SVG信息图
    FE->>U: 展示生成结果
```

#### 3.1.1 模板推荐逻辑

**功能目标**: 基于用户输入的文本内容,智能分析并推荐最适合的信息图模板。

**处理流程**:
1. 接收用户输入的原始文本内容
2. 调用LLM服务分析文本特征(流程类、对比类、时间轴类等)
3. 根据分析结果匹配AntV Infographic内置模板库
4. 返回推荐的top 3-5个模板选项及推荐理由

**LLM Prompt设计要点**:
- 提示词应包含所有可用模板类型的说明
- 要求LLM返回结构化的JSON格式推荐结果
- 包含推荐理由字段,帮助用户理解选择依据

**推荐结果数据结构**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| templateId | string | 模板唯一标识符 |
| templateName | string | 模板中文名称 |
| confidence | number | 推荐置信度(0-1) |
| reason | string | 推荐理由说明 |
| preview | string | 模板预览图URL |

#### 3.1.2 数据结构化逻辑

**功能目标**: 将用户的自然语言文本转换为符合选定模板要求的结构化数据配置。

**处理流程**:
1. 接收用户文本和选定的模板信息
2. 获取该模板所需的数据结构Schema定义
3. 调用LLM服务提取关键信息并映射到数据结构
4. 验证生成的数据是否符合模板Schema要求
5. 返回完整的Infographic配置对象

**LLM Prompt设计要点**:
- 提供明确的模板数据Schema定义
- 要求严格按照JSON Schema输出结构化数据
- 包含数据示例,指导LLM正确理解字段含义
- 处理可能的数据缺失情况,提供合理的默认值

**配置对象结构**:

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| template | string | 是 | 模板标识符 |
| data | object | 是 | 数据内容对象 |
| data.title | string | 否 | 信息图标题 |
| data.desc | string | 否 | 信息图描述 |
| data.items | array | 是 | 数据项列表 |
| themeConfig | object | 否 | 主题配置 |
| width | number/string | 否 | 画布宽度 |
| height | number/string | 否 | 画布高度 |

### 3.2 模板选择功能

**功能目标**: 允许用户浏览、筛选和手动选择信息图模板。

**核心能力**:
- 展示AntV Infographic内置的100+模板
- 支持按类别筛选(流程图、对比图、时间轴等)
- 提供模板预览功能
- 支持模板搜索和收藏

**模板分类体系**:

| 类别 | 说明 | 适用场景 |
|------|------|----------|
| list-row | 横向列表布局 | 流程展示、步骤说明 |
| list-column | 纵向列表布局 | 层级关系、排名展示 |
| pyramid | 金字塔型布局 | 层级结构、优先级展示 |
| hierarchy-tree | 树形层级布局 | 组织架构、分类体系 |
| timeline | 时间轴布局 | 历史进程、项目计划 |
| comparison | 对比型布局 | 优劣对比、差异分析 |

**前端交互设计**:
- 卡片式模板展示,显示预览缩略图和名称
- 分类标签页或侧边栏筛选
- 点击模板卡片展开详情和应用示例
- 支持快速应用到当前内容

### 3.3 样式自定义功能

**功能目标**: 提供可视化的样式配置界面,允许用户自定义信息图的视觉效果。

**可配置项**:

| 配置类别 | 配置项 | 说明 |
|----------|--------|------|
| 颜色方案 | 主题色板 | 预设色板或自定义颜色组合 |
| 颜色方案 | 背景色 | 画布背景颜色 |
| 颜色方案 | 文本色 | 默认文本颜色 |
| 字体设置 | 字体族 | 标题和正文字体选择 |
| 字体设置 | 字号 | 各级文本大小调整 |
| 字体设置 | 字重 | 文本粗细设置 |
| 视觉效果 | 手绘风格 | 启用rough风格渲染 |
| 视觉效果 | 渐变效果 | 启用渐变填充 |
| 视觉效果 | 纹理图案 | 应用纹理背景 |
| 布局调整 | 间距 | 元素间距调整 |
| 布局调整 | 对齐方式 | 内容对齐设置 |

**前端实现方式**:
- 颜色选择器组件用于颜色配置
- 下拉选择器用于字体和预设选项
- 滑块组件用于数值型参数调整
- 开关组件用于布尔型特效开关
- 实时预览,配置变更立即反映在预览区

**样式配置数据结构**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| themeConfig | object | 主题配置根对象 |
| themeConfig.palette | string/array | 色板名称或自定义颜色数组 |
| themeConfig.fontFamily | string | 字体族名称 |
| styleConfig | object | 视觉风格配置 |
| styleConfig.rough | boolean/object | 手绘风格开关或详细配置 |
| styleConfig.gradient | boolean/object | 渐变效果配置 |
| styleConfig.pattern | string/object | 纹理图案配置 |

### 3.4 导出功能

**功能目标**: 支持多种格式的信息图导出,满足不同使用场景需求。

**支持的导出格式**:

| 格式 | 优先级 | 实现方式 | 适用场景 |
|------|--------|----------|----------|
| SVG | 高 | Infographic原生输出 | 矢量图编辑、Web展示 |
| PNG | 高 | SVG转换(canvas/服务端) | 图片分享、文档插入 |
| PDF | 中 | SVG转PDF库 | 打印、文档归档 |
| PPTX | 中 | 可编辑格式生成 | 演示文稿编辑 |

**导出流程设计**:

```mermaid
graph TD
    A[用户触发导出] --> B{选择导出格式}
    B -->|SVG| C[直接获取SVG内容]
    B -->|PNG| D[SVG转Canvas]
    B -->|PDF| E[SVG转PDF]
    B -->|PPTX| F[生成PPTX结构]
    
    C --> G[下载文件]
    D --> H[设置分辨率]
    H --> I[Canvas转Blob]
    I --> G
    
    E --> J[调用PDF生成库]
    J --> G
    
    F --> K[创建PPTX文档对象]
    K --> L[插入SVG为形状/图片]
    L --> M[添加可编辑文本框]
    M --> G
```

**导出配置选项**:

| 格式 | 可配置项 | 说明 |
|------|----------|------|
| PNG | 宽度、高度、DPI | 控制输出图片质量和尺寸 |
| PNG | 背景透明度 | 是否保留透明背景 |
| PDF | 页面尺寸 | A4、Letter等标准尺寸 |
| PDF | 边距设置 | 页面边距配置 |
| PPTX | 幻灯片尺寸 | 16:9或4:3等比例 |
| PPTX | 编辑模式 | 图片模式或可编辑模式 |

**技术实现要点**:
- SVG导出: 直接从Infographic的renderSVG方法获取SVG字符串
- PNG导出: 前端使用html2canvas或canvas API,或后端使用puppeteer/playwright
- PDF导出: 使用jsPDF或pdfkit库
- PPTX导出: 使用pptxgenjs或python-pptx库,需要在后端实现

### 3.5 信息图管理功能

**功能目标**: 提供用户创建的信息图的保存、浏览、编辑和删除功能。

**核心能力**:
- 保存信息图配置和生成结果
- 列表展示历史创建记录
- 支持信息图重新编辑
- 分类和标签管理
- 搜索和筛选功能
- 批量操作(删除、导出)

**数据模型设计**:

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | string | 是 | 唯一标识符 |
| title | string | 是 | 信息图标题 |
| description | string | 否 | 描述信息 |
| originalText | text | 是 | 用户输入的原始文本 |
| config | json | 是 | Infographic完整配置 |
| svgContent | text | 是 | 生成的SVG内容 |
| thumbnail | string | 否 | 缩略图URL |
| tags | array | 否 | 标签列表 |
| category | string | 否 | 分类 |
| createdAt | datetime | 是 | 创建时间 |
| updatedAt | datetime | 是 | 更新时间 |
| userId | string | 是 | 创建用户ID |

**存储策略**:
- 配置数据存储在数据库中(建议使用PostgreSQL或MongoDB)
- SVG内容可存储在数据库或对象存储服务
- 缩略图存储在对象存储服务,加速列表加载

**前端界面设计**:
- 列表视图: 网格或列表展示,显示缩略图、标题、创建时间
- 筛选器: 按时间范围、分类、标签筛选
- 搜索框: 支持标题和描述的全文搜索
- 操作按钮: 编辑、导出、删除、复制等

## 四、AI服务集成设计

### 4.1 AiHubMix配置管理

**配置文件结构** (.env):

```
# AiHubMix LLM配置
AIHUBMIX_API_KEY=your_api_key_here
AIHUBMIX_BASE_URL=https://aihubmix.com/v1
AIHUBMIX_MODEL_RECOMMEND=gpt-4o-mini
AIHUBMIX_MODEL_EXTRACT=gpt-4o-mini
AIHUBMIX_TIMEOUT=30
AIHUBMIX_MAX_RETRIES=3

# 应用配置
APP_NAME=AI信息图生成系统
APP_VERSION=1.0.0
DEBUG_MODE=false

# 数据库配置
DATABASE_URL=postgresql://user:password@localhost/infographic_db

# 文件存储配置
STORAGE_TYPE=local
STORAGE_PATH=/var/data/infographics
```

**配置项说明**:

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| AIHUBMIX_API_KEY | API密钥 | 必填 |
| AIHUBMIX_BASE_URL | API基础URL | https://aihubmix.com/v1 |
| AIHUBMIX_MODEL_RECOMMEND | 模板推荐使用的模型 | gpt-4o-mini |
| AIHUBMIX_MODEL_EXTRACT | 数据提取使用的模型 | gpt-4o-mini |
| AIHUBMIX_TIMEOUT | 请求超时时间(秒) | 30 |
| AIHUBMIX_MAX_RETRIES | 最大重试次数 | 3 |

**安全措施**:
- .env文件不纳入版本控制(.gitignore)
- 提供.env.example模板文件
- 生产环境使用环境变量或密钥管理服务
- API密钥权限控制和额度监控

### 4.2 LLM调用封装

**客户端设计原则**:
- 统一的调用接口,屏蔽底层实现细节
- 支持重试和错误处理机制
- 记录调用日志,便于调试和监控
- 支持流式和非流式两种调用方式

**核心方法定义**:

| 方法名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| recommend_template | user_text: str | List[TemplateRecommendation] | 推荐信息图模板 |
| extract_data | user_text: str, template_schema: dict | dict | 提取结构化数据 |
| chat_completion | messages: List[dict], model: str | str | 通用聊天补全 |

**错误处理策略**:
- API调用失败时自动重试(指数退避)
- 超时错误返回友好提示信息
- 配额不足时提示用户
- 记录错误日志用于问题排查

### 4.3 Prompt工程设计

#### 4.3.1 模板推荐Prompt

**Prompt结构**:
- 系统角色定义: 定位为信息图设计专家
- 任务说明: 分析文本并推荐合适的模板
- 模板列表: 提供完整的可用模板及其适用场景
- 输出格式: JSON Schema定义
- Few-shot示例: 提供2-3个示例

**输出格式要求**:
```
{
  "recommendations": [
    {
      "templateId": "模板ID",
      "templateName": "模板名称",
      "confidence": 0.95,
      "reason": "推荐理由"
    }
  ]
}
```

#### 4.3.2 数据提取Prompt

**Prompt结构**:
- 系统角色定义: 定位为数据分析师
- 任务说明: 从文本中提取信息并结构化
- Schema定义: 提供目标模板的数据结构
- 提取规则: 说明字段含义和填充规则
- 输出格式: 严格的JSON Schema
- Few-shot示例: 针对特定模板的示例

**输出格式要求**:
根据不同模板动态生成,需包含:
- 必填字段验证
- 字段类型约束
- 枚举值限制
- 默认值处理规则

**Prompt优化策略**:
- 定期收集错误案例,优化Prompt
- A/B测试不同Prompt版本
- 根据用户反馈调整推荐逻辑
- 维护Prompt版本管理

## 五、API接口设计

### 5.1 RESTful API规范

**基础路径**: `/api/v1`

**通用响应格式**:

成功响应:
```
{
  "success": true,
  "data": { ... },
  "message": "操作成功"
}
```

错误响应:
```
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "错误描述",
    "details": { ... }
  }
}
```

### 5.2 核心API端点

#### 5.2.1 模板相关API

| 端点 | 方法 | 说明 | 请求参数 | 响应数据 |
|------|------|------|----------|----------|
| /templates | GET | 获取模板列表 | category(可选), search(可选) | 模板列表数组 |
| /templates/{id} | GET | 获取模板详情 | 路径参数: id | 模板详细信息 |
| /templates/recommend | POST | AI推荐模板 | text: 用户文本 | 推荐模板列表 |

**推荐模板接口详细设计**:

请求体:
```
{
  "text": "用户输入的文本内容",
  "maxRecommendations": 5
}
```

响应体:
```
{
  "success": true,
  "data": {
    "recommendations": [
      {
        "templateId": "list-row-horizontal-icon-arrow",
        "templateName": "横向流程图",
        "confidence": 0.92,
        "reason": "文本描述了一个线性流程,适合使用横向箭头展示",
        "preview": "/assets/templates/list-row-horizontal-icon-arrow.png",
        "category": "流程图"
      }
    ],
    "analysisTime": 1.2
  }
}
```

#### 5.2.2 数据生成API

| 端点 | 方法 | 说明 | 请求参数 | 响应数据 |
|------|------|------|----------|----------|
| /generate/extract | POST | 提取结构化数据 | text, templateId | 结构化配置对象 |
| /generate/render | POST | 渲染信息图 | config | SVG内容 |

**数据提取接口详细设计**:

请求体:
```
{
  "text": "用户输入的文本内容",
  "templateId": "list-row-horizontal-icon-arrow"
}
```

响应体:
```
{
  "success": true,
  "data": {
    "config": {
      "template": "list-row-horizontal-icon-arrow",
      "data": {
        "title": "提取的标题",
        "items": [
          {
            "label": "步骤1",
            "desc": "描述内容",
            "icon": "icon:mdi/check"
          }
        ]
      },
      "themeConfig": {
        "palette": "antv"
      }
    },
    "extractionTime": 2.5
  }
}
```

#### 5.2.3 导出API

| 端点 | 方法 | 说明 | 请求参数 | 响应数据 |
|------|------|------|----------|----------|
| /export/svg | POST | 导出SVG | config | SVG文件 |
| /export/png | POST | 导出PNG | config, width, height, dpi | PNG文件流 |
| /export/pdf | POST | 导出PDF | config, pageSize | PDF文件流 |
| /export/pptx | POST | 导出PPTX | config, slideSize, editable | PPTX文件流 |

**导出接口通用设计**:

请求体:
```
{
  "config": { ... },
  "options": {
    "format": "png",
    "width": 1920,
    "height": 1080,
    "dpi": 300,
    "transparent": false
  }
}
```

响应:
- Content-Type: application/octet-stream 或对应的MIME类型
- Content-Disposition: attachment; filename="infographic.png"
- 文件流数据

#### 5.2.4 管理API

| 端点 | 方法 | 说明 | 请求参数 | 响应数据 |
|------|------|------|----------|----------|
| /infographics | GET | 获取信息图列表 | page, pageSize, category, search | 分页列表 |
| /infographics | POST | 保存信息图 | title, config, svgContent, tags | 创建的信息图对象 |
| /infographics/{id} | GET | 获取信息图详情 | 路径参数: id | 信息图详细数据 |
| /infographics/{id} | PUT | 更新信息图 | 完整或部分字段 | 更新后的对象 |
| /infographics/{id} | DELETE | 删除信息图 | 路径参数: id | 删除确认 |

**列表接口详细设计**:

请求参数:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | integer | 否 | 页码,默认1 |
| pageSize | integer | 否 | 每页数量,默认20 |
| category | string | 否 | 分类筛选 |
| tags | string | 否 | 标签筛选,逗号分隔 |
| search | string | 否 | 搜索关键词 |
| sortBy | string | 否 | 排序字段 |
| order | string | 否 | 排序方向(asc/desc) |

响应体:
```
{
  "success": true,
  "data": {
    "items": [ ... ],
    "total": 100,
    "page": 1,
    "pageSize": 20,
    "totalPages": 5
  }
}
```

### 5.3 认证与鉴权

**认证方案**: JWT Token

**认证流程**:
1. 用户登录,后端验证凭证
2. 生成JWT Token返回给前端
3. 前端存储Token(localStorage或Cookie)
4. 后续请求在Header中携带Token
5. 后端验证Token有效性和权限

**Token格式**:
```
Authorization: Bearer <jwt_token>
```

**Token Payload包含**:
- userId: 用户ID
- username: 用户名
- roles: 角色列表
- exp: 过期时间
- iat: 签发时间

**权限控制**:
- 用户只能访问和操作自己创建的信息图
- 管理员可以查看所有信息图
- 导出功能可能需要额外的权限或配额限制

## 六、前端实现设计

### 6.1 技术栈与依赖

**核心依赖**:

| 库名 | 版本 | 用途 |
|------|------|------|
| vue | ^3.4.0 | 前端框架 |
| vue-router | ^4.2.0 | 路由管理 |
| pinia | ^2.1.0 | 状态管理 |
| @antv/infographic | ^0.1.0 | 信息图渲染 |
| axios | ^1.6.0 | HTTP客户端 |
| element-plus | ^2.5.0 | UI组件库(可选) |
| vite | ^5.0.0 | 构建工具 |

### 6.2 页面路由规划

| 路径 | 组件 | 说明 | 权限要求 |
|------|------|------|----------|
| / | Home | 首页/欢迎页 | 公开 |
| /create | CreateInfographic | 创建信息图页面 | 需登录 |
| /manage | ManageInfographics | 信息图管理页面 | 需登录 |
| /edit/:id | EditInfographic | 编辑信息图页面 | 需登录+所有权 |
| /templates | TemplateGallery | 模板浏览页面 | 公开 |
| /login | Login | 登录页面 | 公开 |
| /register | Register | 注册页面 | 公开 |

### 6.3 状态管理设计

**Store模块划分**:

```mermaid
graph LR
    A[Root Store] --> B[User Store]
    A --> C[Template Store]
    A --> D[Infographic Store]
    A --> E[UI Store]
    
    B --> B1[用户信息]
    B --> B2[认证状态]
    
    C --> C1[模板列表]
    C --> C2[当前模板]
    
    D --> D1[当前配置]
    D --> D2[历史记录]
    
    E --> E1[加载状态]
    E --> E2[错误信息]
```

**User Store状态**:
| 状态名 | 类型 | 说明 |
|--------|------|------|
| user | object | 当前用户信息 |
| token | string | 认证Token |
| isAuthenticated | boolean | 登录状态 |

**Template Store状态**:
| 状态名 | 类型 | 说明 |
|--------|------|------|
| templates | array | 模板列表 |
| categories | array | 分类列表 |
| selectedTemplate | object | 当前选中模板 |
| recommendations | array | AI推荐结果 |

**Infographic Store状态**:
| 状态名 | 类型 | 说明 |
|--------|------|------|
| currentConfig | object | 当前信息图配置 |
| currentSVG | string | 生成的SVG内容 |
| userInputText | string | 用户输入文本 |
| infographicList | array | 用户的信息图列表 |

### 6.4 核心组件设计

#### 6.4.1 TextInputPanel组件

**功能**: 提供文本输入和AI分析触发功能

**主要属性**:
| 属性名 | 类型 | 说明 |
|--------|------|------|
| modelValue | string | 双向绑定的文本内容 |
| placeholder | string | 输入提示文本 |
| maxLength | number | 最大字符数限制 |

**主要事件**:
| 事件名 | 参数 | 说明 |
|--------|------|------|
| update:modelValue | string | 文本内容变化 |
| submit | string | 提交文本触发分析 |
| clear | - | 清空文本内容 |

**UI元素**:
- 多行文本输入框(textarea)
- 字符计数显示
- 清空按钮
- 提交/分析按钮
- 示例文本快速填充

#### 6.4.2 TemplateSelector组件

**功能**: 模板浏览和选择

**主要属性**:
| 属性名 | 类型 | 说明 |
|--------|------|------|
| templates | array | 模板列表数据 |
| selectedId | string | 当前选中模板ID |
| viewMode | string | 展示模式(grid/list) |

**主要事件**:
| 事件名 | 参数 | 说明 |
|--------|------|------|
| select | templateId | 选择模板 |
| preview | templateId | 预览模板 |
| filter | filterOptions | 筛选条件变化 |

**UI元素**:
- 分类标签页或筛选器
- 模板卡片网格/列表
- 搜索框
- 视图切换按钮
- 模板预览弹窗

#### 6.4.3 StyleConfigurator组件

**功能**: 可视化样式配置面板

**主要属性**:
| 属性名 | 类型 | 说明 |
|--------|------|------|
| config | object | 当前样式配置 |
| schema | object | 可配置项Schema |

**主要事件**:
| 事件名 | 参数 | 说明 |
|--------|------|------|
| update:config | object | 配置更新 |
| reset | - | 重置为默认值 |

**UI元素**:
- 折叠面板分组(颜色、字体、效果等)
- 颜色选择器
- 字体下拉选择器
- 数值滑块
- 开关按钮
- 预设方案快捷选择

#### 6.4.4 InfographicPreview组件

**功能**: 实时预览信息图渲染结果

**主要属性**:
| 属性名 | 类型 | 说明 |
|--------|------|------|
| config | object | Infographic配置对象 |
| width | number/string | 预览区域宽度 |
| height | number/string | 预览区域高度 |

**主要事件**:
| 事件名 | 参数 | 说明 |
|--------|------|------|
| rendered | svgContent | 渲染完成 |
| error | errorInfo | 渲染错误 |

**核心逻辑**:
- 监听config变化,触发重新渲染
- 使用AntV Infographic的Infographic类
- 处理渲染异常并显示错误提示
- 支持缩放和居中显示

#### 6.4.5 ExportDialog组件

**功能**: 导出选项配置和执行

**主要属性**:
| 属性名 | 类型 | 说明 |
|--------|------|------|
| visible | boolean | 对话框显示状态 |
| config | object | 要导出的配置 |

**主要事件**:
| 事件名 | 参数 | 说明 |
|--------|------|------|
| close | - | 关闭对话框 |
| export | exportOptions | 执行导出 |

**UI元素**:
- 格式选择(SVG/PNG/PDF/PPTX)
- 格式特定选项配置表单
- 文件名输入
- 导出进度提示
- 导出按钮

### 6.5 AntV Infographic集成

**初始化流程**:

```mermaid
graph TD
    A[组件挂载] --> B[创建容器元素]
    B --> C[实例化Infographic]
    C --> D[配置options]
    D --> E[调用render方法]
    E --> F[监听渲染完成]
    F --> G[获取SVG内容]
```

**配置更新机制**:
- 使用Vue的watch监听配置对象变化
- 配置变化时调用Infographic实例的update方法(如提供)或重新render
- 使用防抖优化频繁更新

**销毁处理**:
- 组件卸载时调用Infographic的destroy方法(如提供)
- 清理DOM引用避免内存泄漏

## 七、后端实现设计

### 7.1 技术栈与依赖

**核心依赖**:

| 库名 | 版本 | 用途 |
|------|------|------|
| fastapi | ^0.109.0 | Web框架 |
| uvicorn | ^0.27.0 | ASGI服务器 |
| pydantic | ^2.5.0 | 数据验证 |
| sqlalchemy | ^2.0.0 | ORM |
| python-dotenv | ^1.0.0 | 环境变量加载 |
| httpx | ^0.26.0 | HTTP客户端 |
| python-jose | ^3.3.0 | JWT处理 |
| passlib | ^1.7.4 | 密码哈希 |
| python-multipart | ^0.0.6 | 文件上传 |
| pillow | ^10.2.0 | 图片处理 |
| pptx | ^0.6.21 | PPTX生成 |

### 7.2 项目结构

```
backend/
├── app/
│   ├── main.py                 # 应用入口
│   ├── config.py               # 配置管理
│   ├── dependencies.py         # 依赖注入
│   ├── api/
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── templates.py    # 模板相关端点
│   │   │   ├── generate.py     # 生成相关端点
│   │   │   ├── export.py       # 导出相关端点
│   │   │   ├── infographics.py # 管理相关端点
│   │   │   └── auth.py         # 认证相关端点
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # 用户模型
│   │   ├── infographic.py      # 信息图模型
│   │   └── template.py         # 模板模型
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py             # 用户Schema
│   │   ├── infographic.py      # 信息图Schema
│   │   ├── template.py         # 模板Schema
│   │   └── common.py           # 通用Schema
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm_client.py       # LLM客户端
│   │   ├── template_service.py # 模板服务
│   │   ├── generate_service.py # 生成服务
│   │   ├── export_service.py   # 导出服务
│   │   └── storage_service.py  # 存储服务
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── auth.py             # 认证工具
│   │   ├── prompts.py          # Prompt模板
│   │   └── validators.py       # 验证器
│   └── db/
│       ├── __init__.py
│       ├── base.py             # 数据库基类
│       └── session.py          # 数据库会话
├── tests/
│   ├── __init__.py
│   ├── test_api/
│   └── test_services/
├── .env.example
├── requirements.txt
└── README.md
```

### 7.3 配置管理模块

**config.py设计**:

配置类结构:
| 配置类 | 说明 | 配置项 |
|--------|------|--------|
| Settings | 主配置类 | 所有配置项的汇总 |
| AiHubMixConfig | LLM服务配置 | API密钥、URL、模型等 |
| DatabaseConfig | 数据库配置 | 连接URL、连接池设置 |
| StorageConfig | 存储配置 | 存储类型、路径等 |

**配置加载流程**:
1. 从.env文件读取环境变量
2. 使用Pydantic进行类型验证
3. 提供默认值处理
4. 单例模式确保配置一致性

**配置访问方式**:
通过依赖注入或全局单例访问配置对象

### 7.4 LLM客户端服务

**llm_client.py核心职责**:
- 封装与AiHubMix API的通信
- 管理API密钥和请求头
- 实现重试和超时逻辑
- 提供统一的错误处理

**主要方法**:

| 方法名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| chat_completion | messages, model, temperature | str | 通用聊天补全 |
| recommend_templates | user_text, available_templates | list | 推荐模板 |
| extract_structured_data | user_text, template_schema | dict | 提取结构化数据 |

**调用示例流程**:
1. 构建符合OpenAI格式的messages数组
2. 设置base_url为AiHubMix的端点
3. 使用配置的API密钥
4. 发送请求并处理响应
5. 解析JSON结果并验证格式

**异常处理**:
- APIConnectionError: 网络连接失败
- APITimeoutError: 请求超时
- RateLimitError: 超出配额
- InvalidResponseError: 响应格式错误
- ValidationError: 数据验证失败

### 7.5 模板服务

**template_service.py核心职责**:
- 管理AntV Infographic内置模板信息
- 提供模板查询和筛选功能
- 调用LLM服务进行模板推荐
- 返回模板Schema定义

**模板元数据结构**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | string | 模板唯一标识 |
| name | string | 模板名称 |
| category | string | 所属分类 |
| description | string | 模板描述 |
| dataSchema | object | 数据结构Schema |
| preview | string | 预览图URL |
| tags | array | 标签列表 |
| difficulty | string | 使用难度 |

**模板信息来源**:
- 从AntV Infographic库的getTemplates方法获取
- 补充自定义的元数据(分类、描述等)
- 可存储在数据库或静态配置文件中

### 7.6 生成服务

**generate_service.py核心职责**:
- 调用LLM提取文本中的结构化数据
- 验证生成的配置是否符合模板要求
- 处理配置合并和默认值填充
- 生成Infographic可用的完整配置

**数据提取流程**:

```mermaid
sequenceDiagram
    participant API as API端点
    participant GS as GenerateService
    participant LLM as LLMClient
    participant V as Validator
    
    API->>GS: extract_data(text, template_id)
    GS->>GS: 获取模板Schema
    GS->>LLM: extract_structured_data(text, schema)
    LLM-->>GS: 返回原始数据
    GS->>V: 验证数据格式
    V-->>GS: 验证结果
    alt 验证失败
        GS->>LLM: 重新提取或修正
    end
    GS->>GS: 填充默认值
    GS->>GS: 构建完整配置
    GS-->>API: 返回配置对象
```

**配置验证规则**:
- 必填字段完整性检查
- 数据类型匹配验证
- 枚举值范围验证
- 数组长度限制检查
- 嵌套对象结构验证

### 7.7 导出服务

**export_service.py核心职责**:
- 实现多种格式的导出功能
- 调用外部库进行格式转换
- 管理临时文件生成和清理
- 返回文件流或文件路径

**各格式实现方案**:

| 格式 | 实现方式 | 关键步骤 |
|------|----------|----------|
| SVG | 直接返回 | 从配置生成SVG字符串,直接返回 |
| PNG | 无头浏览器 | 使用playwright渲染HTML+SVG为PNG |
| PDF | SVG转PDF | 使用svglib+reportlab或weasyprint |
| PPTX | python-pptx | 创建演示文稿,插入SVG或PNG |

**PNG导出详细流程**:
1. 将SVG内容嵌入HTML模板
2. 启动无头浏览器(playwright)
3. 加载HTML页面
4. 设置视口尺寸和DPI
5. 截图保存为PNG
6. 返回文件流

**PPTX导出详细流程**:
1. 创建Presentation对象
2. 添加空白幻灯片
3. 转换SVG为图片并插入
4. 如需可编辑,添加文本框和形状
5. 保存为字节流
6. 返回文件流

**资源管理**:
- 使用临时目录存储中间文件
- 导出完成后清理临时文件
- 限制并发导出数量避免资源耗尽

### 7.8 存储服务

**storage_service.py核心职责**:
- 抽象文件存储接口
- 支持本地文件系统和对象存储
- 管理文件上传和下载
- 生成访问URL

**存储接口定义**:

| 方法名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| save | file_content, file_name, folder | file_url | 保存文件 |
| get | file_url | file_content | 获取文件内容 |
| delete | file_url | bool | 删除文件 |
| get_url | file_path | public_url | 生成访问URL |

**本地存储实现**:
- 文件保存在配置的本地目录
- 按日期或用户ID分文件夹存储
- 返回相对路径作为文件URL

**对象存储实现**(可选扩展):
- 支持AWS S3、阿里云OSS等
- 上传文件到对象存储服务
- 返回公开或签名URL

## 八、数据库设计

### 8.1 表结构设计

#### 8.1.1 用户表(users)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | UUID | PRIMARY KEY | 用户ID |
| username | VARCHAR(50) | UNIQUE, NOT NULL | 用户名 |
| email | VARCHAR(100) | UNIQUE, NOT NULL | 邮箱 |
| password_hash | VARCHAR(255) | NOT NULL | 密码哈希 |
| is_active | BOOLEAN | DEFAULT TRUE | 账户状态 |
| created_at | TIMESTAMP | NOT NULL | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL | 更新时间 |

#### 8.1.2 信息图表(infographics)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | UUID | PRIMARY KEY | 信息图ID |
| user_id | UUID | FOREIGN KEY, NOT NULL | 所属用户 |
| title | VARCHAR(200) | NOT NULL | 标题 |
| description | TEXT | - | 描述 |
| original_text | TEXT | NOT NULL | 原始输入文本 |
| config | JSONB | NOT NULL | 完整配置JSON |
| svg_content | TEXT | NOT NULL | SVG内容 |
| thumbnail_url | VARCHAR(500) | - | 缩略图URL |
| template_id | VARCHAR(100) | - | 使用的模板ID |
| category | VARCHAR(50) | - | 分类 |
| tags | TEXT[] | - | 标签数组 |
| is_public | BOOLEAN | DEFAULT FALSE | 是否公开 |
| view_count | INTEGER | DEFAULT 0 | 浏览次数 |
| created_at | TIMESTAMP | NOT NULL | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL | 更新时间 |

#### 8.1.3 模板信息表(templates)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | VARCHAR(100) | PRIMARY KEY | 模板ID |
| name | VARCHAR(100) | NOT NULL | 模板名称 |
| category | VARCHAR(50) | NOT NULL | 分类 |
| description | TEXT | - | 描述 |
| data_schema | JSONB | NOT NULL | 数据结构Schema |
| preview_url | VARCHAR(500) | - | 预览图URL |
| tags | TEXT[] | - | 标签 |
| difficulty | VARCHAR(20) | - | 难度等级 |
| usage_count | INTEGER | DEFAULT 0 | 使用次数 |
| is_active | BOOLEAN | DEFAULT TRUE | 是否启用 |
| created_at | TIMESTAMP | NOT NULL | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL | 更新时间 |

### 8.2 索引设计

**性能优化索引**:

| 表名 | 索引字段 | 类型 | 说明 |
|------|----------|------|------|
| users | email | UNIQUE | 邮箱查询优化 |
| users | username | UNIQUE | 用户名查询优化 |
| infographics | user_id | B-TREE | 用户信息图列表查询 |
| infographics | template_id | B-TREE | 模板使用统计 |
| infographics | category | B-TREE | 分类筛选 |
| infographics | created_at | B-TREE | 时间排序 |
| infographics | tags | GIN | 标签搜索(PostgreSQL) |
| templates | category | B-TREE | 分类查询 |

### 8.3 数据迁移策略

**版本管理**:
使用Alembic进行数据库迁移版本管理

**迁移流程**:
1. 开发环境创建迁移脚本
2. 测试环境验证迁移
3. 生产环境执行迁移
4. 保留回滚脚本

## 九、部署架构设计

### 9.1 部署拓扑

```mermaid
graph TB
    subgraph 客户端
        A[浏览器]
    end
    
    subgraph 负载均衡层
        B[Nginx/负载均衡器]
    end
    
    subgraph 应用层
        C1[Vue前端服务器1]
        C2[Vue前端服务器2]
        D1[FastAPI后端服务1]
        D2[FastAPI后端服务2]
    end
    
    subgraph 数据层
        E[PostgreSQL数据库]
        F[Redis缓存]
    end
    
    subgraph 存储层
        G[文件存储]
    end
    
    subgraph 外部服务
        H[AiHubMix API]
    end
    
    A --> B
    B --> C1
    B --> C2
    C1 --> D1
    C2 --> D2
    D1 --> E
    D2 --> E
    D1 --> F
    D2 --> F
    D1 --> G
    D2 --> G
    D1 --> H
    D2 --> H
```

### 9.2 容器化部署

**Docker镜像构建**:
- 前端: 基于nginx镜像,包含构建后的静态文件
- 后端: 基于python:3.11-slim,包含应用代码和依赖

**Docker Compose配置**:

服务定义:
| 服务名 | 镜像 | 端口 | 依赖 |
|--------|------|------|------|
| frontend | infographic-frontend | 80:80 | - |
| backend | infographic-backend | 8000:8000 | db, redis |
| db | postgres:15 | 5432:5432 | - |
| redis | redis:7 | 6379:6379 | - |

**环境变量管理**:
- 开发环境: .env.development
- 测试环境: .env.testing
- 生产环境: .env.production

### 9.3 性能优化策略

**缓存策略**:
- 模板列表缓存(Redis, TTL 1小时)
- API响应缓存(条件缓存,GET请求)
- 静态资源CDN缓存

**并发处理**:
- FastAPI异步处理提高并发能力
- 数据库连接池优化
- LLM API调用使用异步客户端

**资源限制**:
- 文本输入长度限制(如5000字符)
- 导出文件大小限制
- 并发导出任务队列

## 十、测试策略

### 10.1 测试层级

| 测试类型 | 覆盖范围 | 工具 | 目标 |
|----------|----------|------|------|
| 单元测试 | 函数和类方法 | Vitest(前端), Pytest(后端) | 代码逻辑正确性 |
| 集成测试 | API端点 | Pytest + TestClient | 接口功能完整性 |
| E2E测试 | 用户流程 | Playwright/Cypress | 业务流程可用性 |
| 性能测试 | 系统负载 | Locust/K6 | 并发能力和响应时间 |

### 10.2 关键测试场景

**功能测试**:
- 文本输入和模板推荐准确性
- 数据提取和配置生成正确性
- 信息图渲染效果验证
- 各格式导出功能验证
- 用户权限和数据隔离

**异常测试**:
- LLM API调用失败处理
- 无效配置数据处理
- 网络超时处理
- 并发冲突处理
- 存储空间不足处理

**性能测试**:
- 100并发用户访问
- 大批量信息图列表加载
- 高分辨率导出性能
- 数据库查询性能

## 十一、风险评估与应对

### 11.1 技术风险

| 风险项 | 可能性 | 影响程度 | 应对措施 |
|--------|--------|----------|----------|
| LLM API不稳定 | 中 | 高 | 实现重试机制,提供降级方案,缓存推荐结果 |
| AntV Infographic兼容性 | 低 | 中 | 锁定版本,充分测试,准备迁移方案 |
| 导出性能瓶颈 | 中 | 中 | 异步任务队列,资源限制,优化算法 |
| 数据库性能 | 低 | 中 | 索引优化,读写分离,缓存策略 |

### 11.2 业务风险

| 风险项 | 可能性 | 影响程度 | 应对措施 |
|--------|--------|----------|----------|
| LLM生成质量不稳定 | 中 | 高 | 优化Prompt,提供人工调整,收集反馈优化 |
| API配额超限 | 中 | 高 | 用量监控,用户配额限制,替代方案 |
| 用户数据隐私 | 低 | 高 | 数据加密,访问控制,合规审查 |

### 11.3 应对策略

**降级方案**:
- LLM不可用时,提供手动选择模板和填充数据
- 导出失败时,至少保证SVG格式可用
- 存储故障时,提供临时下载不保存

**监控预警**:
- API调用成功率和响应时间监控
- 错误日志实时告警
- 资源使用率监控

**容灾备份**:
- 数据库定期备份
- 配置文件版本控制
- 关键数据异地备份

## 十二、后续扩展规划

### 12.1 功能扩展

**短期计划**:
- 支持更多导出格式(Word、Excel等)
- 提供信息图模板自定义功能
- 实现协作编辑和分享功能
- 添加信息图动画效果

**长期计划**:
- 构建信息图模板市场
- 支持多语言国际化
- 提供企业级权限管理
- 开发移动端应用

### 12.2 技术优化

**性能提升**:
- 引入WebWorker处理复杂渲染
- 实现增量渲染和虚拟滚动
- 优化大数据量信息图生成

**AI能力增强**:
- 支持多轮对话优化信息图
- 图像识别自动配图
- 智能布局优化建议
- 风格迁移和个性化推荐

**用户体验**:
- 实时协作编辑
- 版本历史和回滚
- 快捷键和操作优化
- 无障碍访问支持
