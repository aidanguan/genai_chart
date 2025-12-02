# genai-chart 部署脚本 (Windows PowerShell版本)
# 用于将项目部署到 genai-dev 服务器的 Docker 环境

$ErrorActionPreference = "Stop"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  AI信息图生成系统 - Docker部署脚本" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# 检查Docker是否运行
Write-Host "`n[1/7] 检查Docker环境..." -ForegroundColor Yellow
try {
    docker info | Out-Null
    Write-Host "✓ Docker环境正常" -ForegroundColor Green
} catch {
    Write-Host "错误: Docker未运行，请先启动Docker服务" -ForegroundColor Red
    exit 1
}

# 检查 .env 文件
Write-Host "`n[2/7] 检查环境变量配置..." -ForegroundColor Yellow
if (-not (Test-Path "backend\.env")) {
    Write-Host "错误: backend\.env 文件不存在" -ForegroundColor Red
    Write-Host "请创建 backend\.env 文件并配置必要的环境变量"
    exit 1
}
Write-Host "✓ 环境变量配置文件存在" -ForegroundColor Green

# 停止并删除旧容器
Write-Host "`n[3/7] 停止旧容器..." -ForegroundColor Yellow
docker-compose -f docker-compose.prod.yml down 2>$null
Write-Host "✓ 旧容器已停止" -ForegroundColor Green

# 清理旧镜像（可选）
$response = Read-Host "是否清理旧的Docker镜像？(y/N)"
if ($response -eq 'y' -or $response -eq 'Y') {
    Write-Host "`n清理旧镜像..." -ForegroundColor Yellow
    docker-compose -f docker-compose.prod.yml rm -f 2>$null
    docker rmi genai_chart-1-backend genai_chart-1-frontend 2>$null
    Write-Host "✓ 旧镜像已清理" -ForegroundColor Green
}

# 构建镜像
Write-Host "`n[4/7] 构建Docker镜像..." -ForegroundColor Yellow
docker-compose -f docker-compose.prod.yml build --no-cache
Write-Host "✓ 镜像构建完成" -ForegroundColor Green

# 初始化数据库（首次部署）
if (-not (Test-Path "backend\data\genai_chart.db")) {
    Write-Host "`n[5/7] 检测到首次部署，初始化数据库..." -ForegroundColor Yellow
    
    # 创建必要的目录
    New-Item -ItemType Directory -Force -Path "backend\data" | Out-Null
    New-Item -ItemType Directory -Force -Path "backend\temp\exports" | Out-Null
    
    # 临时启动后端容器初始化数据库
    Write-Host "正在初始化数据库..."
    docker-compose -f docker-compose.prod.yml run --rm backend python scripts/init_db.py
    
    Write-Host "正在导入模板数据..."
    docker-compose -f docker-compose.prod.yml run --rm backend python scripts/import_templates.py
    
    Write-Host "✓ 数据库初始化完成" -ForegroundColor Green
} else {
    Write-Host "`n[5/7] 数据库已存在，跳过初始化" -ForegroundColor Yellow
}

# 启动容器
Write-Host "`n[6/7] 启动服务..." -ForegroundColor Yellow
docker-compose -f docker-compose.prod.yml up -d
Write-Host "✓ 服务已启动" -ForegroundColor Green

# 等待服务就绪
Write-Host "`n[7/7] 等待服务就绪..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# 检查服务状态
Write-Host "`n检查服务状态..." -ForegroundColor Yellow
docker-compose -f docker-compose.prod.yml ps

# 健康检查
Write-Host "`n执行健康检查..." -ForegroundColor Yellow
$maxRetries = 10
$retryCount = 0

while ($retryCount -lt $maxRetries) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/docs" -UseBasicParsing -TimeoutSec 2
        if ($response.StatusCode -eq 200) {
            Write-Host "✓ 后端服务健康检查通过" -ForegroundColor Green
            break
        }
    } catch {
        $retryCount++
        Write-Host "等待后端服务启动... ($retryCount/$maxRetries)"
        Start-Sleep -Seconds 3
    }
}

if ($retryCount -eq $maxRetries) {
    Write-Host "警告: 后端服务健康检查超时" -ForegroundColor Red
}

# 检查前端
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8080" -UseBasicParsing -TimeoutSec 2
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ 前端服务健康检查通过" -ForegroundColor Green
    }
} catch {
    Write-Host "警告: 前端服务可能未正常启动" -ForegroundColor Red
}

# 部署完成
Write-Host "`n=========================================" -ForegroundColor Green
Write-Host "  部署完成！" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host "`n服务访问地址："
Write-Host "  前端应用: " -NoNewline; Write-Host "http://localhost:8080" -ForegroundColor Green
Write-Host "  后端API:  " -NoNewline; Write-Host "http://localhost:8000" -ForegroundColor Green
Write-Host "  API文档:  " -NoNewline; Write-Host "http://localhost:8000/docs" -ForegroundColor Green
Write-Host "`n常用命令："
Write-Host "  查看日志: " -NoNewline; Write-Host "docker-compose -f docker-compose.prod.yml logs -f" -ForegroundColor Yellow
Write-Host "  停止服务: " -NoNewline; Write-Host "docker-compose -f docker-compose.prod.yml down" -ForegroundColor Yellow
Write-Host "  重启服务: " -NoNewline; Write-Host "docker-compose -f docker-compose.prod.yml restart" -ForegroundColor Yellow
Write-Host "  查看状态: " -NoNewline; Write-Host "docker-compose -f docker-compose.prod.yml ps" -ForegroundColor Yellow
Write-Host ""
