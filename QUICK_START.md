# 快速开始指南

## 🚀 5分钟快速启动

### 前提条件
- Python 3.8+
- Node.js 16+

### 第一步：启动后端

```bash
# 1. 进入后端目录
cd backend

# 2. 安装Python依赖（如果还没安装）
pip install -r requirements.txt

# 3. 初始化数据库（首次运行）
python scripts/init_db.py
python scripts/import_templates.py

# 4. 启动后端服务
python -m app.main
```

✅ 后端运行在: **http://localhost:8000**
📖 API文档: **http://localhost:8000/docs**

### 第二步：启动前端

打开新的终端窗口：

```bash
# 1. 进入前端目录
cd frontend

# 2. 安装依赖（如果还没安装）
npm install

# 3. 启动开发服务器
npm run dev
```

✅ 前端运行在: **http://localhost:5177**

### 第三步：开始使用

1. 打开浏览器访问 **http://localhost:5177**
2. 在左侧输入框中输入内容（例如：公司2023年销售数据，Q1：100万，Q2：150万，Q3：120万，Q4：180万）
3. 点击"分析并推荐模板"按钮
4. 查看右侧生成的信息图
5. 点击"导出"按钮可导出为SVG/PNG/PDF/PPTX
6. 点击"保存"按钮保存到作品库

---

## 📚 功能概览

### 1. AI智能推荐
- 输入文本描述
- AI分析内容类型
- 自动推荐最合适的模板

### 2. 实时预览
- 左右分栏设计
- 实时生成信息图
- 支持模板切换

### 3. 多格式导出
- **SVG** - 矢量图（无需额外依赖）
- **PNG** - 高清位图
- **PDF** - 文档格式
- **PPTX** - 演示文稿

### 4. 作品管理
- 保存生成的信息图
- 查看历史作品
- 重新编辑

---

## 🎨 支持的模板分类

1. **图表型** - 数值展示、趋势分析
2. **对比型** - 优劣对比、差异分析
3. **层级型** - 组织架构、分级结构
4. **列表型** - 要点列举、步骤说明
5. **四象限型** - 矩阵分析、象限划分
6. **关系型** - 因果关系、流程关系
7. **顺序型** - 时间线、流程图

---

## 🔧 导出功能设置（可选）

如果需要PNG/PDF/PPTX导出功能，需要安装额外依赖：

### Windows
```bash
# 下载并安装GTK+ for Windows
# https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases

pip install cairosvg python-pptx
```

### macOS
```bash
brew install cairo pkg-config
pip install cairosvg python-pptx
```

### Linux
```bash
sudo apt-get install libcairo2-dev pkg-config python3-dev
pip install cairosvg python-pptx
```

详见: `EXPORT_DEPENDENCIES.md`

---

## 📖 API文档

后端启动后，访问 **http://localhost:8000/docs** 查看完整API文档（Swagger UI）

主要API端点：
- `/api/v1/templates` - 模板管理
- `/api/v1/generate` - 信息图生成
- `/api/v1/works` - 作品管理
- `/api/v1/export` - 导出功能

---

## ❓ 常见问题

### Q1: 数据库文件在哪里？
A: `backend/infographic.db` (SQLite数据库)

### Q2: 如何添加更多模板？
A: 编辑 `backend/scripts/collect_templates.py`，添加模板数据后运行 `python scripts/import_templates.py`

### Q3: 前端报错找不到模块？
A: 删除 `node_modules` 文件夹，重新运行 `npm install`

### Q4: 后端启动失败？
A: 检查端口8000是否被占用，或修改 `backend/app/main.py` 中的端口配置

### Q5: 导出功能报错？
A: 检查是否安装了cairosvg依赖，SVG导出始终可用

---

## 📞 技术支持

- 查看完整文档: `FINAL_COMPLETION_REPORT.md`
- 导出依赖指南: `EXPORT_DEPENDENCIES.md`
- 查看进度报告: `IMPLEMENTATION_PROGRESS.md`

---

## 🎉 享受使用！

现在您可以开始使用AI信息图生成器了。输入您的数据，让AI帮您创建精美的信息图！
