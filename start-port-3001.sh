#!/bin/bash

# 在3001端口启动GenAI Chart项目

echo "========================================"
echo "  GenAI Chart - 启动在3001端口"
echo "========================================"
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "错误: Docker 未安装"
    exit 1
fi

# 创建Docker网络
echo "创建Docker网络..."
sudo docker network create genai-chart-network 2>/dev/null || echo "网络已存在"

# 停止并删除旧容器
echo "清理旧容器..."
sudo docker stop genai-chart-backend genai-chart-frontend 2>/dev/null
sudo docker rm genai-chart-backend genai-chart-frontend 2>/dev/null

# 构建后端镜像
echo ""
echo "构建后端镜像..."
sudo docker build -f backend/Dockerfile -t genai-chart-backend:latest .

if [ $? -ne 0 ]; then
    echo "后端镜像构建失败"
    exit 1
fi

# 构建前端镜像
echo ""
echo "构建前端镜像..."
sudo docker build -f frontend/Dockerfile -t genai-chart-frontend:latest .

if [ $? -ne 0 ]; then
    echo "前端镜像构建失败"
    exit 1
fi

# 创建数据目录
mkdir -p backend/data backend/temp

# 启动后端容器
echo ""
echo "启动后端容器..."
sudo docker run -d \
  --name genai-chart-backend \
  --network genai-chart-network \
  -p 8001:8000 \
  -v "$(pwd)/backend:/app" \
  -v "$(pwd)/backend/data:/app/data" \
  -v "$(pwd)/backend/temp:/app/temp" \
  --env-file .env \
  genai-chart-backend:latest

if [ $? -ne 0 ]; then
    echo "后端容器启动失败"
    exit 1
fi

# 启动前端容器
echo ""
echo "启动前端容器..."
sudo docker run -d \
  --name genai-chart-frontend \
  --network genai-chart-network \
  -p 3001:80 \
  genai-chart-frontend:latest

if [ $? -ne 0 ]; then
    echo "前端容器启动失败"
    exit 1
fi

# 等待服务启动
echo ""
echo "等待服务启动..."
sleep 5

# 检查容器状态
echo ""
echo "========================================"
echo "  服务状态"
echo "========================================"
echo ""

BACKEND_STATUS=$(sudo docker ps --filter "name=genai-chart-backend" --format "{{.Status}}" 2>/dev/null)
FRONTEND_STATUS=$(sudo docker ps --filter "name=genai-chart-frontend" --format "{{.Status}}" 2>/dev/null)

if [ -n "$BACKEND_STATUS" ]; then
    echo "✓ 后端服务: http://localhost:8001"
    echo "  API 文档: http://localhost:8001/docs"
else
    echo "✗ 后端服务启动失败"
    sudo docker logs genai-chart-backend
fi

if [ -n "$FRONTEND_STATUS" ]; then
    echo "✓ 前端服务: http://localhost:3001"
else
    echo "✗ 前端服务启动失败"
    sudo docker logs genai-chart-frontend
fi

echo ""
echo "========================================"
echo "  常用命令"
echo "========================================"
echo "查看后端日志: sudo docker logs -f genai-chart-backend"
echo "查看前端日志: sudo docker logs -f genai-chart-frontend"
echo "停止服务:     sudo docker stop genai-chart-backend genai-chart-frontend"
echo "重启服务:     sudo docker restart genai-chart-backend genai-chart-frontend"
echo ""
