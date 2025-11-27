#!/bin/bash

# Bash 脚本 - Docker 快速启动脚本 (Linux/macOS)

echo "========================================"
echo "  信息图生成系统 - Docker 部署"
echo "========================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 检查 Docker 是否安装
echo -e "${YELLOW}[1/5] 检查 Docker 环境...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker 未安装，请先安装 Docker${NC}"
    echo -e "${YELLOW}安装指南: https://docs.docker.com/get-docker/${NC}"
    exit 1
fi

DOCKER_VERSION=$(docker --version)
echo -e "${GREEN}✓ Docker 已安装: $DOCKER_VERSION${NC}"

# 检查 .env 文件
echo ""
echo -e "${YELLOW}[2/5] 检查环境配置...${NC}"
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠ 未找到 .env 文件，使用默认配置${NC}"
    
    if [ -f "backend/.env" ]; then
        cp backend/.env .env
        echo -e "${GREEN}✓ 已从 backend/.env 复制配置${NC}"
    else
        echo -e "${RED}! 请手动创建 .env 文件并配置 API Key${NC}"
        echo -e "${YELLOW}  示例内容:${NC}"
        echo -e "  AIHUBMIX_API_KEY=your_api_key"
        echo -e "  AIHUBMIX_BASE_URL=https://aihubmix.com/v1"
        
        read -p "是否继续启动？(y/n): " continue
        if [ "$continue" != "y" ]; then
            exit 0
        fi
    fi
else
    echo -e "${GREEN}✓ 环境配置文件已存在${NC}"
fi

# 停止现有容器
echo ""
echo -e "${YELLOW}[3/5] 停止现有容器...${NC}"
docker-compose down 2>/dev/null
echo -e "${GREEN}✓ 清理完成${NC}"

# 构建镜像
echo ""
echo -e "${YELLOW}[4/5] 构建 Docker 镜像...${NC}"
echo -e "这可能需要几分钟时间，请耐心等待..."
docker-compose build --no-cache
if [ $? -ne 0 ]; then
    echo -e "${RED}✗ 构建失败${NC}"
    exit 1
fi
echo -e "${GREEN}✓ 镜像构建成功${NC}"

# 启动服务
echo ""
echo -e "${YELLOW}[5/5] 启动服务...${NC}"
docker-compose up -d
if [ $? -ne 0 ]; then
    echo -e "${RED}✗ 启动失败${NC}"
    exit 1
fi

# 等待服务就绪
echo ""
echo -e "${YELLOW}等待服务启动...${NC}"
sleep 5

# 检查服务状态
BACKEND_STATUS=$(docker ps --filter "name=genai-chart-backend" --format "{{.Status}}" 2>/dev/null)
FRONTEND_STATUS=$(docker ps --filter "name=genai-chart-frontend" --format "{{.Status}}" 2>/dev/null)

echo ""
echo "========================================"
echo -e "  ${GREEN}部署完成！${NC}"
echo "========================================"
echo ""

if [ -n "$BACKEND_STATUS" ]; then
    echo -e "${GREEN}✓ 后端服务:${NC} ${CYAN}http://localhost:8000${NC}"
    echo -e "  API 文档: ${CYAN}http://localhost:8000/docs${NC}"
else
    echo -e "${RED}✗ 后端服务启动失败${NC}"
fi

if [ -n "$FRONTEND_STATUS" ]; then
    echo -e "${GREEN}✓ 前端服务:${NC} ${CYAN}http://localhost${NC}"
else
    echo -e "${RED}✗ 前端服务启动失败${NC}"
fi

echo ""
echo "========================================"
echo -e "  ${YELLOW}功能特性${NC}"
echo "========================================"
echo -e "${GREEN}✓ PNG 导出 - 高清位图${NC}"
echo -e "${GREEN}✓ SVG 导出 - 矢量图形${NC}"
echo -e "${GREEN}✓ PPTX 导出 - PowerPoint (Cairo 已安装)${NC}"
echo -e "${GREEN}✓ AI 智能推荐${NC}"
echo -e "${GREEN}✓ 作品管理${NC}"
echo ""

echo "========================================"
echo -e "  ${YELLOW}常用命令${NC}"
echo "========================================"
echo -e "查看日志:     docker-compose logs -f"
echo -e "停止服务:     docker-compose down"
echo -e "重启服务:     docker-compose restart"
echo -e "进入后端容器: docker-compose exec backend bash"
echo ""

echo -e "${GREEN}祝使用愉快！${NC}"
echo ""
