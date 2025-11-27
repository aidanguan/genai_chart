# AI信息图生成系统 v2.0

基于AntV Infographic和大语言模型的智能信息图生成系统

## 系统简介

本系统是一个Web应用,用户只需输入文本内容,系统会通过AI自动分析并推荐合适的信息图模板,提取结构化数据,最终生成专业的信息图。

### 核心功能

1. **AI模板推荐**: 根据文本内容智能推荐最合适的信息图模板
2. **智能数据提取**: 自动从文本中提取关键信息并结构化
3. **信息图生成**: 使用AntV Infographic渲染专业信息图
4. **多格式导出**: 支持导出SVG、PNG、PDF、PPTX等格式 ✨新增
5. **模板分类系统**: 7大分类，100+模板数据库 ✨新增
6. **作品管理**: 保存和管理你的信息图作品 ✨新增
7. **AI工作区**: 左右分栏，实时预览，操作简单 ✨新增

### 技术栈

- **前端**: Vue 3 + TypeScript + Vite + Pinia + Vue Router + Ant Design Vue
- **后端**: Python + FastAPI + SQLAlchemy + SQLite/PostgreSQL
- **可视化**: AntV Infographic
- **AI服务**: AiHubMix (兼容OpenAI API)
- **导出**: cairosvg + python-pptx

## 快速开始

> 🚀 **推荐阅读**: [QUICK_START.md](QUICK_START.md) - 5分钟快速启动指南

> 📚 **完整文档**: [FINAL_COMPLETION_REPORT.md](FINAL_COMPLETION_REPORT.md) - 查看所有功能详情

### 前置要求

- Node.js 18+
- Python 3.11+
- npm或yarn

### 1. 克隆项目

```bash
cd c:\AI\genai_chart-1
```

### 2. 后端配置

#### 安装Python依赖

```bash
cd backend
pip install -r requirements.txt
```

#### 配置环境变量

复制`.env.example`为`.env`,并填写配置:

```bash
cp .env.example .env
```

编辑`.env`文件,填入你的AiHubMix API密钥:

```
AIHUBMIX_API_KEY=你的API密钥
AIHUBMIX_BASE_URL=https://aihubmix.com/v1
AIHUBMIX_MODEL_RECOMMEND=gpt-4o-mini
AIHUBMIX_MODEL_EXTRACT=gpt-4o-mini
DEBUG_MODE=true
```

#### 启动后端服务

```bash
# 在backend目录下

# 1. 首次运行需要初始化数据库 ✨新增
python scripts/init_db.py
python scripts/import_templates.py

# 2. 启动服务
python -m app.main

# 或使用uvicorn
uvicorn app.main:app --reload --port 8000
```

后端服务将运行在: `http://localhost:8000`

API文档地址: `http://localhost:8000/docs`

### 3. 前端配置

#### 安装依赖

```bash
cd frontend
npm install
```

#### 启动开发服务器

```bash
npm run dev
```

前端服务将运行在: `http://localhost:5173`

## 使用指南

### 1. 使用AI工作区 (推荐) ✨新增

1. 访问 `http://localhost:5177`
2. 在左侧输入框中输入内容
3. 点击“分析并推荐模板”按钮
4. 查看推荐结果，选择喜欢的模板
5. 右侧实时预览生成的信息图
6. 点击“导出”按钮选择格式 (SVG/PNG/PDF/PPTX)
7. 点击“保存”按钮保存到作品库

### 2. 使用经典创建页面

1. 访问 `http://localhost:5173`
2. 点击"开始创建"按钮
3. 在文本框输入要生成信息图的文本内容
4. 点击"分析并推荐模板",AI会推荐合适的模板
5. 选择一个推荐的模板
6. 点击"生成信息图"
7. 查看生成的信息图,可下载SVG格式

### 2. API使用

#### 获取模板列表

```bash
GET /api/v1/templates
```

#### AI推荐模板

```bash
POST /api/v1/templates/recommend
Content-Type: application/json

{
  "text": "用户输入的文本",
  "maxRecommendations": 5
}
```

#### 提取结构化数据

```bash
POST /api/v1/generate/extract
Content-Type: application/json

{
  "text": "用户输入的文本",
  "templateId": "list-row-horizontal-icon-arrow"
}
```

## 项目结构

```
genai_chart-1/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── api/v1/         # API端点
│   │   ├── services/       # 业务服务
│   │   ├── schemas/        # 数据模型
│   │   ├── models/         # 数据库模型
│   │   ├── repositories/   # 数据访问层
│   │   ├── utils/          # 工具函数
│   │   ├── config/         # 配置管理
│   │   └── main.py         # 应用入口
│   ├── scripts/            # 数据库脚本
│   ├── requirements.txt    # Python依赖
│   ├── .env.example        # 环境变量示例
│   └── Dockerfile          # Docker配置
│
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── api/           # API调用
│   │   ├── stores/        # Pinia状态管理
│   │   ├── views/         # 页面组件
│   │   ├── router/        # 路由配置
│   │   └── App.vue        # 根组件
│   ├── package.json       # 前端依赖
│   ├── vite.config.ts     # Vite配置
│   └── Dockerfile         # Docker配置
│
├── antv_infographic/      # AntV Infographic库源码
│   └── infographic/       # 核心库
│
├── docs/                  # 项目文档
│   ├── QUICK_START.md              # 快速开始指南
│   ├── DOCKER_QUICKSTART.md        # Docker快速启动
│   ├── FINAL_COMPLETION_REPORT.md  # 项目完成报告
│   ├── SMART_GENERATION_GUIDE.md   # 智能生成指南
│   ├── TEMPLATE_EXPANSION_GUIDE.md # 模板扩展指南
│   └── ... 更多文档
│
├── tests/                 # 测试文件
│   ├── backend/          # 后端测试
│   │   ├── test_*.py    # 各类测试脚本
│   │   └── check_*.py   # 验证脚本
│   └── frontend/         # 前端测试
│
├── archive/              # 归档文件
│   ├── temp_files/      # 临时测试文件
│   └── old_docs/        # 旧文档
│
├── docker-compose.yml    # Docker编排配置
└── README.md            # 项目说明
```

## 核心流程

### 文本转信息图流程

```
用户输入文本
    ↓
调用LLM分析文本特征
    ↓
推荐合适的模板(top 3-5个)
    ↓
用户选择模板
    ↓
调用LLM提取结构化数据
    ↓
使用AntV Infographic渲染
    ↓
展示信息图/导出
```

## 常见问题

### 1. 后端启动失败

- 检查Python版本是否>=3.11
- 确认已安装所有依赖: `pip install -r requirements.txt`
- 检查`.env`文件配置是否正确

### 2. 前端无法连接后端

- 确认后端服务已启动在8000端口
- 检查CORS配置是否正确
- 查看浏览器控制台错误信息

### 3. AI推荐失败

- 检查AiHubMix API密钥是否正确
- 确认API配额是否充足
- 查看后端日志了解详细错误

### 4. 信息图渲染失败

- 确认AntV Infographic库已正确安装
- 检查生成的配置数据格式是否正确
- 查看浏览器控制台错误信息

## 开发说明

### 项目文档

完整的项目文档位于 `docs/` 目录：

- **快速开始**
  - `QUICK_START.md` - 5分钟快速启动指南
  - `DOCKER_QUICKSTART.md` - Docker快速部署
  
- **功能指南**
  - `SMART_GENERATION_GUIDE.md` - 智能生成功能详解
  - `TEMPLATE_EXPANSION_GUIDE.md` - 模板扩展指南
  - `PPTX_EXPORT_WINDOWS_GUIDE.md` - Windows导出PPTX配置
  - `LLM_PROVIDER_CONFIG.md` - LLM提供商配置
  
- **项目报告**
  - `FINAL_COMPLETION_REPORT.md` - 项目完成总结
  - `PROJECT_STATUS.md` - 项目状态
  - `TASKS_COMPLETED.md` - 已完成任务清单

### 测试说明

所有测试脚本位于 `tests/` 目录：

- **后端测试** (`tests/backend/`)
  - `test_smart_generation.py` - 智能生成流程测试
  - `test_chart_column_simple.py` - 图表模板测试
  - `test_pyramid_e2e.py` - 金字塔模板端到端测试
  - `test_dify_integration.py` - Dify工作流集成测试
  - `test_pptx_chinese.py` - PPTX中文导出测试
  - `check_*.py` - 各种配置验证脚本

### 添加新模板

1. 在`backend/app/services/template_service.py`的`TEMPLATE_METADATA`中添加模板元数据
2. 在`backend/app/utils/prompts.py`的`TEMPLATE_SCHEMAS`中定义数据结构
3. 重启后端服务

### 自定义Prompt

编辑`backend/app/utils/prompts.py`中的提示词模板,优化AI推荐和数据提取效果。

## 许可证

MIT License

## 联系方式

- 项目地址: c:\AI\genai_chart-1
- AntV Infographic官网: https://infographic.antv.vision/
- AiHubMix文档: https://docs.aihubmix.com/

## 致谢

- [AntV Infographic](https://github.com/antvis/infographic) - 信息图渲染引擎
- [FastAPI](https://fastapi.tiangolo.com/) - 现代化Python Web框架  
- [Vue 3](https://vuejs.org/) - 渐进式JavaScript框架
- [AiHubMix](https://aihubmix.com/) - LLM API服务提供商
