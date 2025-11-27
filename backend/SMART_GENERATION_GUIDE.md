# 智能生成功能使用指南

## 概述

新的智能生成功能采用三阶段流程，能够自动识别用户文本的内容类型、选择最合适的模板、并提取结构化数据生成信息图配置。

## 功能特性

### 7大图表类型分类

系统支持自动识别以下7种图表类型：

| 类型代码 | 中文名称 | 典型特征 | 适用场景 |
|---------|---------|---------|---------|
| chart | 图表型 | 包含数值数据、统计信息 | 销售数据、用户增长、KPI指标 |
| comparison | 对比型 | 两个或多个事物的对比 | 产品对比、竞品分析、SWOT分析 |
| hierarchy | 层级型 | 上下级、父子关系 | 组织架构、知识体系、产品分类 |
| list | 列表型 | 并列项目、要点、特性 | 功能列表、要点罗列、步骤说明 |
| quadrant | 四象限型 | 两个维度划分 | 优先级矩阵、时间管理、风险评估 |
| relationship | 关系型 | 元素间的关联、因果 | 业务流程、系统架构、关系网络 |
| sequence | 顺序型 | 先后顺序、时间线 | 操作流程、项目进度、历史进程 |

### 三阶段智能流程

1. **类型识别**：分析文本内容特征，识别最适合的图表类型
2. **模板选择**：从该类型的所有模板中选择最匹配的一个
3. **数据提取**：根据模板的数据结构Schema提取关键信息

## 部署步骤

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

新增依赖：`PyYAML==6.0.1`

### 2. 数据库迁移

运行迁移脚本添加新字段：

```bash
cd backend
python scripts/add_template_category_fields.py
```

该脚本会：
- 添加 `structure_type` 字段
- 添加 `keywords` 字段
- 更新 `category` 字段注释
- 创建相关索引

### 3. 模板分类初始化

运行分类脚本为所有模板自动分类：

```bash
cd backend
python scripts/init_template_categories.py
```

该脚本会：
- 读取所有现有模板
- 根据structure类型自动分类
- 更新数据库中的分类信息
- 输出分类统计

### 4. 提示词配置（可选）

提示词配置文件位于 `backend/app/config/llm_prompts.yaml`

您可以通过以下方式自定义提示词：

#### 方式1：修改YAML配置文件

编辑 `backend/app/config/llm_prompts.yaml`

#### 方式2：使用环境变量（优先级更高）

在 `.env` 文件中添加：

```bash
# LLM提示词配置
LLM_TYPE_CLASSIFICATION_SYSTEM_PROMPT="你是一位专业的信息图分类专家..."
LLM_TEMPLATE_SELECTION_SYSTEM_PROMPT="你是一位专业的信息图设计专家..."
LLM_DATA_EXTRACTION_SYSTEM_PROMPT="你是一位专业的数据分析师..."

# 可选：调整温度参数
LLM_TYPE_CLASSIFICATION_TEMPERATURE=0.3
LLM_TEMPLATE_SELECTION_TEMPERATURE=0.3
LLM_DATA_EXTRACTION_TEMPERATURE=0.2
```

## API使用

### 智能生成端点（推荐）

**端点**: `POST /api/v1/generate/smart`

**请求**:
```json
{
  "text": "产品开发流程包括：需求分析、设计、开发、测试、上线五个阶段"
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "config": {
      // AntV Infographic配置对象，可直接用于渲染
      "template": "sequence-timeline-simple",
      "data": {
        "title": "产品开发流程",
        "items": [...]
      },
      "themeConfig": {...}
    },
    "classification": {
      "type": "sequence",
      "confidence": 0.95,
      "reason": "文本包含明确的步骤顺序和流程描述"
    },
    "selection": {
      "templateId": "sequence-timeline-simple",
      "templateName": "简单时间轴",
      "confidence": 0.92,
      "reason": "用户文本描述了按时间顺序的事件，时间轴模板最适合"
    },
    "timing": {
      "phase1_classification": 1.23,
      "phase2_selection": 0.95,
      "phase3_extraction": 1.45,
      "total": 3.63
    }
  },
  "message": "智能生成成功"
}
```

### 传统提取端点（向后兼容）

**端点**: `POST /api/v1/generate/extract`

**请求**:
```json
{
  "text": "产品开发流程...",
  "templateId": "sequence-timeline-simple"
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "config": {...},
    "extractionTime": 1.45
  }
}
```

## 测试

### 运行集成测试

```bash
cd backend
python test_smart_generation.py
```

测试覆盖：
- 类型识别服务测试
- 模板选择服务测试
- 完整三阶段流程测试
- 多种类型的示例文本测试

### 测试用例示例

测试脚本包含以下场景：

1. **顺序型**："产品开发流程包括：需求分析、设计、开发、测试、上线五个阶段"
2. **列表型**："我们的产品有五大核心功能：智能推荐、数据分析、用户管理、报表生成、权限控制"
3. **对比型**："产品A的优势：价格便宜、功能丰富。产品B的优势：性能更好、界面更美观"
4. **层级型**："公司组织架构：CEO下设三个部门，技术部门、市场部门、运营部门"

## 前端集成

### 使用新API

更新前端API调用：

```typescript
// 智能生成
const response = await fetch('/api/v1/generate/smart', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    text: userInputText
  })
});

const result = await response.json();

if (result.success) {
  const { config, classification, selection, timing } = result.data;
  
  // 显示识别的类型和选择的模板
  console.log(`识别类型: ${classification.type}`);
  console.log(`选择模板: ${selection.templateId}`);
  
  // 使用config渲染信息图
  renderInfographic(config);
}
```

### 显示处理过程（可选）

可以向用户展示AI的分析过程：

```typescript
// 显示类型识别结果
showClassification({
  type: classification.type,
  confidence: classification.confidence,
  reason: classification.reason
});

// 显示模板选择结果
showTemplateSelection({
  templateName: selection.templateName,
  reason: selection.reason
});

// 显示性能统计
showTiming({
  total: timing.total,
  breakdown: [
    `类型识别: ${timing.phase1_classification}s`,
    `模板选择: ${timing.phase2_selection}s`,
    `数据提取: ${timing.phase3_extraction}s`
  ]
});
```

## 优化提示词

### 调优建议

1. **类型识别提示词**：
   - 如果某类型识别不准确，可以在prompt中增加更多该类型的示例
   - 调整temperature参数（默认0.3），更高的值会增加创造性

2. **模板选择提示词**：
   - 可以在prompt中强调某些选择策略（如优先选择简单模板）
   - 根据实际使用情况调整选择权重

3. **数据提取提示词**：
   - 针对特定模板添加更详细的字段说明
   - 提供示例数据帮助LLM理解格式

### 提示词模板变量

配置文件中可使用以下变量：

**类型识别**:
- `{user_text}`: 用户输入的文本

**模板选择**:
- `{user_text}`: 用户输入的文本
- `{content_type}`: 已识别的内容类型
- `{templates_list}`: 格式化的模板列表

**数据提取**:
- `{user_text}`: 用户输入的文本
- `{template_id}`: 目标模板ID
- `{schema}`: 模板的数据结构Schema

## 故障排查

### 常见问题

**1. 数据库迁移失败**
- 检查数据库连接配置
- 确保有足够的权限执行ALTER TABLE
- 查看错误日志确认具体问题

**2. 模板分类不准确**
- 检查模板的designConfig中是否包含structure.type
- 运行分类脚本查看分类统计
- 必要时手动修正数据库中的category和structure_type

**3. LLM返回格式错误**
- 检查提示词是否明确要求返回JSON格式
- 查看LLM响应日志
- 尝试调整temperature参数

**4. 性能问题**
- 考虑使用更快的模型（如gpt-4o-mini）
- 优化提示词长度，减少token消耗
- 实施缓存机制（未来优化）

## 性能优化建议

1. **并行处理**（未来优化）：
   - 对于某些场景，可以并行执行模板推荐和数据提取

2. **缓存机制**（未来优化）：
   - 对相似文本的类型识别结果进行缓存
   - 使用文本向量化计算相似度

3. **模型选择**：
   - 类型识别和模板选择可使用更快的模型
   - 数据提取使用精度更高的模型

## 版本历史

### v1.0.0 (当前版本)
- ✅ 三阶段智能生成流程
- ✅ 7大图表类型自动分类
- ✅ 提示词配置化管理
- ✅ 向后兼容传统API
- ✅ 完整的集成测试套件

### 未来计划
- 用户反馈学习机制
- 智能缓存优化
- Web界面提示词管理
- A/B测试支持
