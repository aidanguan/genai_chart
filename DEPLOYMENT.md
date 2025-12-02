# Docker 部署指南

## 概述

本指南介绍如何将 AI信息图生成系统 部署到 genai-dev 服务器的 Docker 环境中。

## 前置要求

1. **服务器环境**
   - Docker 已安装并运行 (版本 20.10+)
   - Docker Compose 已安装 (版本 1.29+)
   - 确保服务器有足够的资源：
     - 内存: 至少 4GB
     - 磁盘空间: 至少 10GB

2. **端口要求**
   - 8000: 后端 API 服务
   - 8080: 前端 Web 应用

3. **环境变量配置**
   - 确保 `backend/.env` 文件已正确配置

## 快速部署

### 方法 1: 使用自动部署脚本（推荐）

#### Linux/Mac 环境

```bash
# 1. 进入项目目录
cd /path/to/genai_chart-1

# 2. 给脚本添加执行权限
chmod +x deploy-docker.sh

# 3. 运行部署脚本
./deploy-docker.sh
```

#### Windows PowerShell 环境

```powershell
# 1. 进入项目目录
cd C:\path\to\genai_chart-1

# 2. 运行部署脚本
.\deploy-docker.ps1
```

### 方法 2: 手动部署

#### 步骤 1: 准备环境变量

确保 `backend/.env` 文件包含以下配置：

```env
# AiHubMix LLM配置
AIHUBMIX_API_KEY=sk-d6PCSAS2rGrEPb0192B24b54DdE14412Aa0c813bB4EeCc2d
AIHUBMIX_BASE_URL=https://aihubmix.com/v1
AIHUBMIX_MODEL_RECOMMEND=gpt-5.1
AIHUBMIX_MODEL_EXTRACT=gpt-5.1

# Dify工作流配置
DIFY_API_BASE_URL=https://dify-uat.42lab.cn/v1
DIFY_API_KEY=app-ufCoCpuVJbL627fuaBC61KHT

# 应用配置
DEBUG_MODE=false
ALLOWED_ORIGINS=http://localhost:8080,http://your-domain.com
```

#### 步骤 2: 构建并启动服务

```bash
# 停止旧容器（如果存在）
docker-compose -f docker-compose.prod.yml down

# 构建镜像
docker-compose -f docker-compose.prod.yml build

# 启动服务
docker-compose -f docker-compose.prod.yml up -d
```

#### 步骤 3: 初始化数据库（首次部署）

```bash
# 检查数据库是否存在
if [ ! -f "backend/data/genai_chart.db" ]; then
    # 初始化数据库
    docker-compose -f docker-compose.prod.yml run --rm backend python scripts/init_db.py
    
    # 导入模板数据
    docker-compose -f docker-compose.prod.yml run --rm backend python scripts/import_templates.py
fi
```

#### 步骤 4: 验证部署

```bash
# 查看服务状态
docker-compose -f docker-compose.prod.yml ps

# 查看日志
docker-compose -f docker-compose.prod.yml logs -f
```

访问以下地址验证：
- 前端应用: http://localhost:8080
- 后端 API: http://localhost:8000
- API 文档: http://localhost:8000/docs

## 服务管理

### 查看服务状态

```bash
docker-compose -f docker-compose.prod.yml ps
```

### 查看日志

```bash
# 查看所有服务日志
docker-compose -f docker-compose.prod.yml logs -f

# 查看后端日志
docker-compose -f docker-compose.prod.yml logs -f backend

# 查看前端日志
docker-compose -f docker-compose.prod.yml logs -f frontend
```

### 重启服务

```bash
# 重启所有服务
docker-compose -f docker-compose.prod.yml restart

# 重启后端
docker-compose -f docker-compose.prod.yml restart backend

# 重启前端
docker-compose -f docker-compose.prod.yml restart frontend
```

### 停止服务

```bash
docker-compose -f docker-compose.prod.yml stop
```

### 完全停止并删除容器

```bash
docker-compose -f docker-compose.prod.yml down
```

### 更新服务

```bash
# 1. 停止服务
docker-compose -f docker-compose.prod.yml down

# 2. 拉取最新代码
git pull

# 3. 重新构建镜像
docker-compose -f docker-compose.prod.yml build --no-cache

# 4. 启动服务
docker-compose -f docker-compose.prod.yml up -d
```

## 数据持久化

以下数据会持久化存储在宿主机：

- `backend/data/`: 数据库文件
- `backend/temp/`: 临时文件和导出文件

**重要**: 部署前请备份这些目录！

## 健康检查

系统内置健康检查功能：

- **后端**: 每30秒检查一次 `/docs` 端点
- **前端**: 每30秒检查一次首页

查看健康状态：

```bash
docker inspect genai-chart-backend | grep -A 10 Health
docker inspect genai-chart-frontend | grep -A 10 Health
```

## 故障排查

### 容器无法启动

1. 检查 Docker 是否运行：
   ```bash
   docker info
   ```

2. 检查端口是否被占用：
   ```bash
   # Linux/Mac
   netstat -tuln | grep -E '8000|8080'
   
   # Windows
   netstat -ano | findstr -E "8000 8080"
   ```

3. 查看容器日志：
   ```bash
   docker-compose -f docker-compose.prod.yml logs
   ```

### 后端 API 无法访问

1. 检查后端容器状态：
   ```bash
   docker-compose -f docker-compose.prod.yml ps backend
   ```

2. 查看后端日志：
   ```bash
   docker-compose -f docker-compose.prod.yml logs backend
   ```

3. 进入容器检查：
   ```bash
   docker exec -it genai-chart-backend bash
   ```

### 前端页面无法加载

1. 检查前端容器状态：
   ```bash
   docker-compose -f docker-compose.prod.yml ps frontend
   ```

2. 检查 nginx 配置：
   ```bash
   docker exec -it genai-chart-frontend cat /etc/nginx/conf.d/default.conf
   ```

3. 查看前端日志：
   ```bash
   docker-compose -f docker-compose.prod.yml logs frontend
   ```

### 数据库问题

1. 检查数据库文件是否存在：
   ```bash
   ls -la backend/data/genai_chart.db
   ```

2. 重新初始化数据库（会清空现有数据）：
   ```bash
   docker-compose -f docker-compose.prod.yml run --rm backend python scripts/init_db.py
   docker-compose -f docker-compose.prod.yml run --rm backend python scripts/import_templates.py
   ```

### 中文字体显示问题

如果导出的图片中文显示为方块：

1. 检查字体配置：
   ```bash
   docker exec -it genai-chart-backend fc-list | grep -i noto
   ```

2. 重新构建镜像：
   ```bash
   docker-compose -f docker-compose.prod.yml build --no-cache backend
   ```

## 性能优化

### 调整资源限制

编辑 `docker-compose.prod.yml`，添加资源限制：

```yaml
services:
  backend:
    # ... 其他配置 ...
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

### 日志轮转

添加日志配置防止日志文件过大：

```yaml
services:
  backend:
    # ... 其他配置 ...
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## 安全建议

1. **不要将 `.env` 文件提交到版本控制系统**
2. **定期更新 API 密钥**
3. **配置防火墙规则，只开放必要的端口**
4. **使用 HTTPS（生产环境建议使用 nginx 反向代理）**
5. **定期备份数据库文件**

## 生产环境建议

### 使用 Nginx 反向代理

创建 `nginx-proxy.conf`：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 后端 API
    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 启用 HTTPS

使用 Let's Encrypt 免费证书：

```bash
sudo certbot --nginx -d your-domain.com
```

## 监控

### 使用 Docker Stats 监控资源使用

```bash
docker stats genai-chart-backend genai-chart-frontend
```

### 查看容器资源使用

```bash
docker-compose -f docker-compose.prod.yml top
```

## 联系支持

如遇到问题，请提供以下信息：

1. Docker 版本: `docker --version`
2. Docker Compose 版本: `docker-compose --version`
3. 操作系统信息
4. 完整的错误日志
5. 容器状态: `docker-compose -f docker-compose.prod.yml ps`

## 更新日志

- **v1.0.0** (2024-12-02): 初始部署文档
