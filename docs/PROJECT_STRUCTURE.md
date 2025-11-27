# 项目结构说明

## 目录组织

本项目已经过系统整理，采用清晰的目录结构组织代码和文档。

### 核心目录

#### 📁 backend/
后端服务代码，基于 FastAPI 框架

```
backend/
├── app/                    # 应用核心代码
│   ├── api/v1/            # REST API 端点
│   ├── config/            # 配置管理
│   ├── models/            # 数据库模型
│   ├── repositories/      # 数据访问层
│   ├── schemas/           # Pydantic 数据模型
│   ├── services/          # 业务逻辑服务
│   └── utils/             # 工具函数
├── scripts/               # 数据库初始化和维护脚本
├── .env                   # 环境变量配置（不提交到git）
├── .env.example           # 环境变量示例
├── requirements.txt       # Python 依赖
└── Dockerfile             # Docker 镜像配置
```

**关键文件：**
- `app/main.py` - 应用入口
- `app/config/settings.py` - 配置管理
- `scripts/init_db.py` - 数据库初始化
- `scripts/import_templates.py` - 导入模板数据

#### 📁 frontend/
前端应用代码，基于 Vue 3 + TypeScript

```
frontend/
├── src/
│   ├── api/              # API 调用封装
│   ├── router/           # Vue Router 路由配置
│   ├── stores/           # Pinia 状态管理
│   ├── views/            # 页面组件
│   ├── App.vue           # 根组件
│   └── main.ts           # 应用入口
├── package.json          # 前端依赖
├── vite.config.ts        # Vite 构建配置
└── Dockerfile            # Docker 镜像配置
```

#### 📁 antv_infographic/
AntV Infographic 信息图渲染库源码

```
antv_infographic/
└── infographic/
    ├── src/              # 源代码
    ├── esm/              # ES Module 构建产物
    ├── lib/              # CommonJS 构建产物
    └── dev/              # 开发环境
```

### 文档目录

#### 📁 docs/
项目文档集中存放

**快速开始类：**
- `QUICK_START.md` - 5分钟快速启动
- `DOCKER_QUICKSTART.md` - Docker 快速部署
- `DOCKER_DEPLOYMENT.md` - Docker 详细部署指南

**功能指南类：**
- `SMART_GENERATION_GUIDE.md` - 智能生成功能详解
- `TEMPLATE_EXPANSION_GUIDE.md` - 模板扩展指南
- `TEMPLATE_EXPANSION_SUCCESS.md` - 模板扩展成功案例
- `PPTX_EXPORT_WINDOWS_GUIDE.md` - Windows PPTX 导出配置
- `LLM_PROVIDER_CONFIG.md` - LLM 提供商配置说明
- `EXPORT_DEPENDENCIES.md` - 导出功能依赖说明

**技术报告类：**
- `FINAL_COMPLETION_REPORT.md` - 项目完成总结报告
- `PROJECT_STATUS.md` - 项目当前状态
- `PROJECT_DELIVERY.md` - 项目交付文档
- `PYRAMID_BADGE_FIX_REPORT.md` - 金字塔模板修复报告
- `TEMPLATE_BATCH2_SUCCESS.md` - 模板批次2成功报告
- `TEMPLATE_EXPANSION_FINAL_REPORT.md` - 模板扩展最终报告

**任务记录类：**
- `TASKS_COMPLETED.md` - 已完成任务清单
- `TASK_COMPLETION_SUMMARY.md` - 任务完成总结
- `IMPLEMENTATION_PROGRESS.md` - 实施进度
- `INTEGRATION_TEST_REPORT.md` - 集成测试报告

**技术方案类：**
- `SVG_PPT兼容性解决方案.md` - SVG 到 PPT 兼容性方案
- `SVG_PPT_兼容性修复说明.md` - SVG PPT 兼容性修复说明

### 测试目录

#### 📁 tests/
测试脚本和验证工具

```
tests/
├── backend/              # 后端测试
│   ├── test_smart_generation.py       # 智能生成流程测试
│   ├── test_chart_column_simple.py    # 图表模板测试
│   ├── test_pyramid_e2e.py            # 金字塔模板端到端测试
│   ├── test_dify_integration.py       # Dify 工作流集成测试
│   ├── test_dify_simple.py            # Dify 简单测试
│   ├── test_pptx_chinese.py           # PPTX 中文导出测试
│   ├── test_backend_svg_conversion.py # SVG 转换测试
│   ├── check_config.py                # 配置检查
│   ├── check_templates.py             # 模板检查
│   ├── check_pyramid_badge.py         # 金字塔模板检查
│   ├── verify_svg_ppt_compatibility.py # SVG PPT 兼容性验证
│   └── ... 更多测试脚本
└── frontend/            # 前端测试（待添加）
```

**测试分类：**

1. **功能测试**
   - `test_smart_generation.py` - 三阶段智能生成完整流程
   - `test_chart_column_simple.py` - 柱状图模板专项测试
   - `test_pyramid_e2e.py` - 金字塔层级模板端到端测试

2. **集成测试**
   - `test_dify_integration.py` - Dify 工作流 API 集成
   - `test_dify_simple.py` - Dify 基础连接测试
   - `test_backend.py` - 后端基础功能测试

3. **导出功能测试**
   - `test_pptx_chinese.py` - PPTX 中文字体支持测试
   - `test_backend_svg_conversion.py` - SVG 转换功能测试

4. **配置验证**
   - `check_config.py` - 环境配置验证
   - `check_templates.py` - 模板数据完整性检查
   - `check_workflow_config.py` - 工作流配置检查

5. **工具脚本**
   - `add_zigzag_template.py` - 添加 Z 字形模板
   - `fix_pyramid_badge.py` - 修复金字塔徽章模板
   - `update_zigzag_template.py` - 更新 Z 字形模板

### 归档目录

#### 📁 archive/
临时文件和旧版本归档

```
archive/
├── temp_files/          # 临时测试文件
│   ├── *.pptx          # 测试生成的 PPTX 文件
│   ├── *.svg           # 测试 SVG 文件
│   ├── *.png           # 测试图片
│   ├── *.log           # 测试日志
│   └── *.json          # 测试数据
└── old_docs/           # 旧版本文档（如需要）
```

## 配置文件

### 环境配置

- **后端环境变量** (`backend/.env`)
  ```
  AIHUBMIX_API_KEY=你的API密钥
  AIHUBMIX_BASE_URL=https://aihubmix.com/v1
  DIFY_API_KEY=你的Dify API密钥
  DIFY_API_BASE_URL=https://api.dify.ai/v1
  DATABASE_URL=sqlite:///./infographic.db
  ```

- **Docker 配置** (`docker-compose.yml`)
  - 统一管理前后端服务
  - 自动网络配置
  - 数据持久化

### 启动脚本

- `start-docker.sh` - Linux/Mac Docker 启动脚本
- `start-docker.ps1` - Windows Docker 启动脚本

## 数据库

### SQLite 数据库文件

- `backend/infographic.db` - 主数据库
  - `templates` 表 - 模板元数据
  - `works` 表 - 用户作品
  - `template_categories` 表 - 模板分类

### 初始化脚本

```bash
# 初始化数据库
python backend/scripts/init_db.py

# 导入模板数据
python backend/scripts/import_templates.py

# 初始化模板分类
python backend/scripts/init_template_categories.py
```

## 日志文件

日志文件位置（运行时生成）：
- `backend/logs/` - 后端日志
- `frontend/logs/` - 前端日志（如配置）

## Git 版本控制

### 忽略文件 (.gitignore)

**后端忽略：**
- `.env` - 环境变量
- `*.db` - 数据库文件
- `__pycache__/` - Python 缓存
- `*.pyc` - 编译的 Python 文件
- `.venv/` - 虚拟环境

**前端忽略：**
- `node_modules/` - 依赖包
- `dist/` - 构建产物
- `.env.local` - 本地环境变量

**通用忽略：**
- `archive/` - 归档文件
- `*.log` - 日志文件
- `.DS_Store` - Mac 系统文件

## 运行命令

### 开发模式

**后端：**
```bash
cd backend
python -m app.main
# 或
uvicorn app.main:app --reload --port 8000
```

**前端：**
```bash
cd frontend
npm run dev
```

### Docker 模式

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 测试运行

```bash
# 运行智能生成测试
python tests/backend/test_smart_generation.py

# 运行 Dify 集成测试
python tests/backend/test_dify_integration.py

# 运行配置检查
python tests/backend/check_config.py
```

## 开发工作流

1. **开发新功能**
   - 在 `backend/app/` 或 `frontend/src/` 中编写代码
   - 编写相应的测试脚本放在 `tests/` 目录
   - 更新相关文档到 `docs/` 目录

2. **测试功能**
   - 运行单元测试
   - 运行集成测试
   - 手动测试验证

3. **文档更新**
   - 更新功能文档
   - 更新 README.md
   - 记录重要变更

4. **提交代码**
   - Git commit 提交
   - 清理临时文件到 archive/
   - 保持项目结构整洁

## 维护建议

### 定期清理

1. **临时文件**
   - 定期检查 `archive/temp_files/`
   - 删除不需要的测试文件

2. **日志文件**
   - 定期归档或删除旧日志
   - 保持日志目录整洁

3. **数据库**
   - 定期备份数据库文件
   - 清理测试数据

### 文档更新

1. 每次功能变更后更新相关文档
2. 保持 README.md 与实际代码同步
3. 在 `docs/` 中记录重要技术决策

### 测试维护

1. 新功能必须有对应测试
2. 定期运行所有测试确保通过
3. 失效的测试及时修复或删除

---

**整理日期：** 2025-11-27  
**项目版本：** v2.0  
**维护者：** Qoder AI Assistant
