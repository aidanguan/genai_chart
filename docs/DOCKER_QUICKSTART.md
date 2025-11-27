# 🐳 Docker 快速启动指南

## ⚡ 最快启动方式

### Windows 用户

```powershell
# 1. 确保 Docker Desktop 正在运行
# 2. 在项目根目录执行
.\start-docker.ps1
```

### Linux/macOS 用户

```bash
# 1. 确保 Docker 已启动
# 2. 在项目根目录执行
chmod +x start-docker.sh
./start-docker.sh
```

---

## 📦 手动启动

如果启动脚本无法运行，可以手动执行以下命令：

### 第一次启动（构建镜像）

```bash
# 1. 复制环境配置文件
cp backend/.env .env

# 2. 编辑 .env 文件，填入你的 API Key
# AIHUBMIX_API_KEY=your_api_key_here

# 3. 构建并启动
docker-compose up --build -d
```

### 后续启动

```bash
# 直接启动
docker-compose up -d

# 查看日志
docker-compose logs -f
```

---

## 🎯 访问地址

启动成功后：

- **前端界面**：http://localhost
- **后端 API 文档**：http://localhost:8000/docs
- **健康检查**：http://localhost:8000/health

---

## ✅ 功能验证

### 测试 PPTX 导出

```bash
# 进入后端容器
docker-compose exec backend bash

# 测试 Cairo 库
python -c "import cairocffi; print('✓ Cairo 库已安装')"

# 测试 PPTX 导出
python -c "
from app.services.export_service import get_export_service
svg = '<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"100\" height=\"100\"><circle cx=\"50\" cy=\"50\" r=\"40\" fill=\"blue\"/></svg>'
service = get_export_service()
result = service.export_pptx(svg, title='测试', filename='test.pptx')
print('✓ PPTX 导出成功:', result)
"
```

### 在浏览器中测试

1. 打开 http://localhost
2. 输入测试内容
3. 点击"分析并推荐模板"
4. 点击"导出" → "📊 PPTX 演示"
5. 验证文件下载成功

---

## 🛠️ 常用命令

```bash
# 查看运行状态
docker-compose ps

# 查看实时日志
docker-compose logs -f

# 查看后端日志
docker-compose logs -f backend

# 查看前端日志
docker-compose logs -f frontend

# 重启服务
docker-compose restart

# 停止服务
docker-compose down

# 停止并删除数据
docker-compose down -v

# 重新构建
docker-compose build --no-cache
```

---

## 🔧 故障排查

### 问题 1：端口被占用

**错误**：`bind: address already in used`

**解决**：修改 `docker-compose.yml` 中的端口映射

```yaml
services:
  backend:
    ports:
      - "8001:8000"  # 改为 8001
  frontend:
    ports:
      - "8080:80"    # 改为 8080
```

### 问题 2：容器无法启动

**排查步骤**：

```bash
# 1. 查看详细日志
docker-compose logs backend

# 2. 检查容器状态
docker-compose ps

# 3. 重新构建
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### 问题 3：数据库未初始化

```bash
# 进入容器初始化数据库
docker-compose exec backend python scripts/init_db.py
```

---

## 📊 性能监控

```bash
# 查看资源使用情况
docker stats

# 查看容器详情
docker inspect genai-chart-backend
docker inspect genai-chart-frontend
```

---

## 🔄 更新代码

```bash
# 1. 拉取最新代码
git pull

# 2. 重新构建并启动
docker-compose up --build -d

# 3. 查看日志确认启动成功
docker-compose logs -f
```

---

## 🎉 优势总结

### ✅ 使用 Docker 的好处

1. **PPTX 导出开箱即用** - Cairo 库已预装，无需手动配置
2. **环境一致** - 开发、测试、生产环境完全相同
3. **快速部署** - 一条命令启动所有服务
4. **易于维护** - 版本管理和回滚简单
5. **跨平台** - Windows、Linux、macOS 统一部署方式
6. **隔离干净** - 不污染本地开发环境

### 📋 支持的功能

- ✅ PNG 导出（高清位图）
- ✅ SVG 导出（矢量图形）
- ✅ **PPTX 导出（PowerPoint）** - Cairo 已安装
- ✅ AI 智能推荐
- ✅ 模板管理
- ✅ 作品保存

---

## 💡 建议

- **生产环境**：推荐使用 Docker 部署
- **开发环境**：可以使用 Docker，也可以本地运行
- **Windows 用户**：强烈推荐使用 Docker，避免 Cairo 安装问题

---

## 📚 更多信息

- 详细部署文档：[DOCKER_DEPLOYMENT.md](./DOCKER_DEPLOYMENT.md)
- Windows PPTX 配置：[PPTX_EXPORT_WINDOWS_GUIDE.md](./PPTX_EXPORT_WINDOWS_GUIDE.md)
- 项目说明：[README.md](./README.md)

---

**祝使用愉快！** 🎊
