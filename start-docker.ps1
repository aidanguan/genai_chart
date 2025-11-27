# PowerShell 脚本 - Docker 快速启动脚本

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  信息图生成系统 - Docker 部署" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Docker 是否安装
Write-Host "[1/5] 检查 Docker 环境..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "✓ Docker 已安装: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker 未安装，请先安装 Docker Desktop" -ForegroundColor Red
    Write-Host "下载地址: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# 检查 .env 文件
Write-Host ""
Write-Host "[2/5] 检查环境配置..." -ForegroundColor Yellow
if (-Not (Test-Path ".env")) {
    Write-Host "⚠ 未找到 .env 文件，使用默认配置" -ForegroundColor Yellow
    
    # 从 backend/.env 复制
    if (Test-Path "backend\.env") {
        Copy-Item "backend\.env" ".env"
        Write-Host "✓ 已从 backend/.env 复制配置" -ForegroundColor Green
    } else {
        Write-Host "! 请手动创建 .env 文件并配置 API Key" -ForegroundColor Red
        Write-Host "  示例内容:" -ForegroundColor Yellow
        Write-Host "  AIHUBMIX_API_KEY=your_api_key" -ForegroundColor Gray
        Write-Host "  AIHUBMIX_BASE_URL=https://aihubmix.com/v1" -ForegroundColor Gray
        
        $continue = Read-Host "是否继续启动？(y/n)"
        if ($continue -ne "y") {
            exit 0
        }
    }
} else {
    Write-Host "✓ 环境配置文件已存在" -ForegroundColor Green
}

# 停止现有容器
Write-Host ""
Write-Host "[3/5] 停止现有容器..." -ForegroundColor Yellow
docker-compose down 2>$null
Write-Host "✓ 清理完成" -ForegroundColor Green

# 构建镜像
Write-Host ""
Write-Host "[4/5] 构建 Docker 镜像..." -ForegroundColor Yellow
Write-Host "这可能需要几分钟时间，请耐心等待..." -ForegroundColor Gray
docker-compose build --no-cache
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ 构建失败" -ForegroundColor Red
    exit 1
}
Write-Host "✓ 镜像构建成功" -ForegroundColor Green

# 启动服务
Write-Host ""
Write-Host "[5/5] 启动服务..." -ForegroundColor Yellow
docker-compose up -d
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ 启动失败" -ForegroundColor Red
    exit 1
}

# 等待服务就绪
Write-Host ""
Write-Host "等待服务启动..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# 检查服务状态
$backendRunning = docker ps --filter "name=genai-chart-backend" --format "{{.Status}}" 2>$null
$frontendRunning = docker ps --filter "name=genai-chart-frontend" --format "{{.Status}}" 2>$null

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  部署完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($backendRunning) {
    Write-Host "✓ 后端服务: " -NoNewline -ForegroundColor Green
    Write-Host "http://localhost:8000" -ForegroundColor Cyan
    Write-Host "  API 文档: " -NoNewline
    Write-Host "http://localhost:8000/docs" -ForegroundColor Cyan
} else {
    Write-Host "✗ 后端服务启动失败" -ForegroundColor Red
}

if ($frontendRunning) {
    Write-Host "✓ 前端服务: " -NoNewline -ForegroundColor Green
    Write-Host "http://localhost" -ForegroundColor Cyan
} else {
    Write-Host "✗ 前端服务启动失败" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  功能特性" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✓ PNG 导出 - 高清位图" -ForegroundColor Green
Write-Host "✓ SVG 导出 - 矢量图形" -ForegroundColor Green
Write-Host "✓ PPTX 导出 - PowerPoint (Cairo 已安装)" -ForegroundColor Green
Write-Host "✓ AI 智能推荐" -ForegroundColor Green
Write-Host "✓ 作品管理" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  常用命令" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "查看日志:     " -NoNewline
Write-Host "docker-compose logs -f" -ForegroundColor Gray
Write-Host "停止服务:     " -NoNewline
Write-Host "docker-compose down" -ForegroundColor Gray
Write-Host "重启服务:     " -NoNewline
Write-Host "docker-compose restart" -ForegroundColor Gray
Write-Host "进入后端容器: " -NoNewline
Write-Host "docker-compose exec backend bash" -ForegroundColor Gray
Write-Host ""

# 询问是否打开浏览器
$openBrowser = Read-Host "是否在浏览器中打开应用？(y/n)"
if ($openBrowser -eq "y") {
    Start-Process "http://localhost"
}

Write-Host ""
Write-Host "祝使用愉快！" -ForegroundColor Green
Write-Host ""
