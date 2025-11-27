# Docker 部署指南

## ✨ 优势

使用 Docker 部署有以下优势：

1. ✅ **自动包含 Cairo 库** - 无需手动安装，PPTX 导出开箱即用
2. ✅ **环境一致性** - 开发、测试、生产环境完全一致
3. ✅ **快速部署** - 一键启动所有服务
4. ✅ **易于维护** - 版本管理、回滚更简单
5. ✅ **跨平台** - Windows、macOS、Linux 统一部署方式

---

## 📋 前置要求

### 安装 Docker

**Windows/macOS**：
- 下载并安装 [Docker Desktop](https://www.docker.com/products/docker-desktop)
- 启动 Docker Desktop

**Linux**：
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装 Docker Compose
sudo apt-get install docker-compose-plugin
```

### 验证安装
```bash
docker --version
docker-compose --version
```

---

## 🚀 快速启动

### 1. 配置环境变量

创建 `.env` 文件（在项目根目录）：

```bash
# LLM API 配置
AIHUBMIX_API_KEY=your_api_key_here
AIHUBMIX_BASE_URL=https://aihubmix.com/v1
LLM_MODEL=gpt-4o

# Dify 工作流配置（可选）
DIFY_API_KEY=your_dify_key_here
DIFY_BASE_URL=https://dify-uat.42lab.cn/v1
```

### 2. 构建并启动服务

```bash
# 构建镜像并启动所有服务
docker-compose up --build -d

# 查看日志
docker-compose logs -f

# 仅查看后端日志
docker-compose logs -f backend

# 仅查看前端日志
docker-compose logs -f frontend
```

### 3. 访问应用

- **前端界面**：http://localhost
- **后端 API 文档**：http://localhost:8000/docs
- **后端健康检查**：http://localhost:8000/health

### 4. 停止服务

```bash
# 停止所有服务
docker-compose down

# 停止并删除数据卷
docker-compose down -v
```

---

## 🔧 开发模式

### 方式一：使用 Docker Compose（推荐）

修改 `docker-compose.yml` 中的 volumes 配置，启用热重载：

```yaml
services:
  backend:
    # ... existing config ...
    volumes:
      - ./backend:/app  # 代码热重载
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 方式二：混合模式

后端使用 Docker，前端本地运行：

```bash
# 启动后端
docker-compose up backend -d

# 前端本地运行
cd frontend
npm install
npm run dev
```

---

## 📊 验证 PPTX 导出功能

### 进入容器测试

```bash
# 进入后端容器
docker-compose exec backend bash

# 测试 Cairo 库
python -c "import cairocffi; print('Cairo 库已安装!')"

# 测试 PPTX 导出
python -c "
from app.services.export_service import get_export_service

svg = '<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"100\" height=\"100\"><circle cx=\"50\" cy=\"50\" r=\"40\" fill=\"blue\"/></svg>'

service = get_export_service()
result = service.export_pptx(svg, title='测试', filename='test.pptx')
print('✅ PPTX 导出成功:', result)
"
```

### 在应用中测试

1. 打开浏览器访问 http://localhost
2. 输入内容并生成信息图
3. 点击"导出" → "📊 PPTX 演示"
4. 文件会自动下载

---

## 🐛 故障排除

### 问题 1：端口被占用

**错误信息**：
```
Error starting userland proxy: listen tcp4 0.0.0.0:8000: bind: address already in use
```

**解决方法**：
```bash
# 修改 docker-compose.yml 中的端口映射
ports:
  - "8001:8000"  # 改为 8001
```

### 问题 2：容器启动失败

```bash
# 查看详细日志
docker-compose logs backend

# 重新构建
docker-compose build --no-cache backend
docker-compose up -d
```

### 问题 3：数据库初始化

```bash
# 进入容器初始化数据库
docker-compose exec backend python scripts/init_db.py
```

### 问题 4：清理并重置

```bash
# 停止并删除所有容器、网络、卷
docker-compose down -v

# 删除镜像
docker-compose down --rmi all

# 重新构建
docker-compose up --build -d
```

---

## 📦 生产部署

### 1. 使用独立的数据库

修改 `docker-compose.yml`：

```yaml
services:
  # 添加 PostgreSQL
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: genai_chart
      POSTGRES_USER: genai
      POSTGRES_PASSWORD: your_secure_password
    volumes:
      - postgres-data:/var/lib/postgresql/data

  backend:
    # ... existing config ...
    environment:
      - DATABASE_URL=postgresql://genai:your_secure_password@db:5432/genai_chart
    depends_on:
      - db

volumes:
  postgres-data:
```

### 2. 使用 Nginx 反向代理

创建 `nginx-proxy.conf`：

```nginx
upstream backend {
    server backend:8000;
}

upstream frontend {
    server frontend:80;
}

server {
    listen 80;
    server_name your-domain.com;

    # 前端
    location / {
        proxy_pass http://frontend;
    }

    # 后端 API
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. 启用 HTTPS

使用 Let's Encrypt：

```yaml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./ssl:/etc/nginx/ssl
```

---

## 🔍 监控和日志

### 查看实时日志

```bash
# 所有服务
docker-compose logs -f

# 特定服务
docker-compose logs -f backend

# 最近 100 行
docker-compose logs --tail=100 backend
```

### 资源使用情况

```bash
# 查看容器状态
docker-compose ps

# 查看资源使用
docker stats
```

---

## 🎯 性能优化

### 1. 多阶段构建（已实现）

前端 Dockerfile 使用多阶段构建，减小镜像大小。

### 2. 使用缓存

```bash
# 使用构建缓存
docker-compose build

# 强制重新构建
docker-compose build --no-cache
```

### 3. 限制资源

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

---

## ✅ 验证清单

部署完成后，验证以下功能：

- [ ] 前端页面可访问（http://localhost）
- [ ] 后端 API 文档可访问（http://localhost:8000/docs）
- [ ] 数据库连接正常
- [ ] 模板加载成功
- [ ] AI 智能生成功能正常
- [ ] PNG 导出正常
- [ ] SVG 导出正常
- [ ] **PPTX 导出正常** ✨
- [ ] 作品保存功能正常

---

## 📚 常用命令

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看日志
docker-compose logs -f

# 进入容器
docker-compose exec backend bash

# 重新构建
docker-compose build --no-cache

# 清理未使用的镜像
docker image prune -a

# 查看所有容器
docker ps -a

# 删除所有停止的容器
docker container prune
```

---

## 🎉 总结

使用 Docker 部署后：

✅ **PPTX 导出功能完全可用** - Cairo 库已自动安装  
✅ **一键启动** - `docker-compose up -d`  
✅ **环境隔离** - 不影响本地开发环境  
✅ **易于扩展** - 可轻松添加数据库、缓存等服务  

现在您可以享受完整的功能，包括 PPTX 导出！
