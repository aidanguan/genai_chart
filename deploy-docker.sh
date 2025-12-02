#!/bin/bash

# genai-chart 部署脚本
# 用于将项目部署到 genai-dev 服务器的 Docker 环境

set -e

echo "========================================="
echo "  AI信息图生成系统 - Docker部署脚本"
echo "========================================="

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查Docker是否运行
echo -e "\n${YELLOW}[1/7]${NC} 检查Docker环境..."
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}错误: Docker未运行，请先启动Docker服务${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker环境正常${NC}"

# 检查 .env 文件
echo -e "\n${YELLOW}[2/7]${NC} 检查环境变量配置..."
if [ ! -f "backend/.env" ]; then
    echo -e "${RED}错误: backend/.env 文件不存在${NC}"
    echo "请创建 backend/.env 文件并配置必要的环境变量"
    exit 1
fi
echo -e "${GREEN}✓ 环境变量配置文件存在${NC}"

# 停止并删除旧容器
echo -e "\n${YELLOW}[3/7]${NC} 停止旧容器..."
docker-compose -f docker-compose.prod.yml down 2>/dev/null || true
echo -e "${GREEN}✓ 旧容器已停止${NC}"

# 清理旧镜像（可选）
read -p "是否清理旧的Docker镜像？(y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "\n${YELLOW}清理旧镜像...${NC}"
    docker-compose -f docker-compose.prod.yml rm -f 2>/dev/null || true
    docker rmi genai_chart-1-backend genai_chart-1-frontend 2>/dev/null || true
    echo -e "${GREEN}✓ 旧镜像已清理${NC}"
fi

# 构建镜像
echo -e "\n${YELLOW}[4/7]${NC} 构建Docker镜像..."
docker-compose -f docker-compose.prod.yml build --no-cache
echo -e "${GREEN}✓ 镜像构建完成${NC}"

# 初始化数据库（首次部署）
if [ ! -f "backend/data/genai_chart.db" ]; then
    echo -e "\n${YELLOW}[5/7]${NC} 检测到首次部署，初始化数据库..."
    
    # 创建必要的目录
    mkdir -p backend/data backend/temp/exports
    
    # 临时启动后端容器初始化数据库
    echo "正在初始化数据库..."
    docker-compose -f docker-compose.prod.yml run --rm backend python scripts/init_db.py
    
    echo "正在导入模板数据..."
    docker-compose -f docker-compose.prod.yml run --rm backend python scripts/import_templates.py
    
    echo -e "${GREEN}✓ 数据库初始化完成${NC}"
else
    echo -e "\n${YELLOW}[5/7]${NC} 数据库已存在，跳过初始化"
fi

# 启动容器
echo -e "\n${YELLOW}[6/7]${NC} 启动服务..."
docker-compose -f docker-compose.prod.yml up -d
echo -e "${GREEN}✓ 服务已启动${NC}"

# 等待服务就绪
echo -e "\n${YELLOW}[7/7]${NC} 等待服务就绪..."
sleep 5

# 检查服务状态
echo -e "\n${YELLOW}检查服务状态...${NC}"
docker-compose -f docker-compose.prod.yml ps

# 健康检查
echo -e "\n${YELLOW}执行健康检查...${NC}"
max_retries=10
retry_count=0

while [ $retry_count -lt $max_retries ]; do
    if curl -f http://localhost:8000/docs > /dev/null 2>&1; then
        echo -e "${GREEN}✓ 后端服务健康检查通过${NC}"
        break
    fi
    retry_count=$((retry_count + 1))
    echo "等待后端服务启动... ($retry_count/$max_retries)"
    sleep 3
done

if [ $retry_count -eq $max_retries ]; then
    echo -e "${RED}警告: 后端服务健康检查超时${NC}"
fi

# 检查前端
if curl -f http://localhost:8080 > /dev/null 2>&1; then
    echo -e "${GREEN}✓ 前端服务健康检查通过${NC}"
else
    echo -e "${RED}警告: 前端服务可能未正常启动${NC}"
fi

# 部署完成
echo -e "\n${GREEN}=========================================${NC}"
echo -e "${GREEN}  部署完成！${NC}"
echo -e "${GREEN}=========================================${NC}"
echo -e "\n服务访问地址："
echo -e "  前端应用: ${GREEN}http://localhost:8080${NC}"
echo -e "  后端API:  ${GREEN}http://localhost:8000${NC}"
echo -e "  API文档:  ${GREEN}http://localhost:8000/docs${NC}"
echo -e "\n常用命令："
echo -e "  查看日志: ${YELLOW}docker-compose -f docker-compose.prod.yml logs -f${NC}"
echo -e "  停止服务: ${YELLOW}docker-compose -f docker-compose.prod.yml down${NC}"
echo -e "  重启服务: ${YELLOW}docker-compose -f docker-compose.prod.yml restart${NC}"
echo -e "  查看状态: ${YELLOW}docker-compose -f docker-compose.prod.yml ps${NC}"
echo ""
