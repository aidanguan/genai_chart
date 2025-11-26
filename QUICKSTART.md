# 快速启动指南

## 使用前准备

1. **配置AiHubMix API密钥**
   
   编辑 `backend\.env` 文件,将 `AIHUBMIX_API_KEY` 替换为你的真实API密钥:
   ```
   AIHUBMIX_API_KEY=sk-你的真实密钥
   ```

2. **安装后端Python依赖**
   ```powershell
   cd backend
   pip install -r requirements.txt
   ```

3. **安装前端依赖**
   ```powershell
   cd frontend  
   npm install
   ```

## 启动系统

### 方式1: 分别启动(推荐用于开发)

**启动后端:**
```powershell
# 在backend目录下
python -m app.main
```
后端将运行在: http://localhost:8000  
API文档: http://localhost:8000/api/v1/docs

**启动前端:**
```powershell
# 在frontend目录下  
npm run dev
```
前端将运行在: http://localhost:5173

### 方式2: 使用PowerShell脚本一键启动

创建 `start.ps1` 文件并运行:

```powershell
# start.ps1
# 启动后端
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; python -m app.main"

# 等待1秒
Start-Sleep -Seconds 1

# 启动前端
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host "系统启动完成!"
Write-Host "前端地址: http://localhost:5173"
Write-Host "后端API文档: http://localhost:8000/api/v1/docs"
```

运行:
```powershell
.\start.ps1
```

## 使用流程

1. 访问 http://localhost:5173
2. 点击"开始创建"
3. 输入要生成信息图的文本内容(例如:"软件开发分为需求分析、设计、编码、测试、部署五个阶段")
4. 点击"分析并推荐模板"
5. 选择AI推荐的模板
6. 点击"生成信息图"
7. 查看生成的信息图,可下载SVG格式

## 测试示例文本

### 示例1: 流程类
```
软件开发生命周期包含以下关键阶段：需求分析阶段收集和分析用户需求；设计阶段制定系统架构和详细设计；编码阶段进行程序开发；测试阶段验证软件质量；部署阶段将软件发布到生产环境。
```

### 示例2: 层级类  
```
企业组织架构从上到下分为：最高层是董事会负责战略决策；管理层包括CEO和各部门总监；执行层由各部门经理组成；基层员工负责具体业务执行。
```

### 示例3: 时间轴类
```
互联网技术演进史：1991年万维网诞生开启互联网时代；2004年Web 2.0概念提出实现用户交互；2010年移动互联网爆发改变生活方式；2020年AI技术融入互联网应用。
```

## 常见问题

### Q: 后端启动报错 "ModuleNotFoundError"
A: 确保已安装所有依赖: `pip install -r requirements.txt`

### Q: 前端无法连接后端  
A: 检查后端是否正常运行在8000端口,查看后端控制台是否有错误

### Q: AI推荐失败
A: 
1. 检查`.env`文件中的API密钥是否正确
2. 确认AiHubMix账户余额是否充足
3. 查看后端控制台的详细错误信息

### Q: 信息图无法显示
A: 
1. 打开浏览器开发者工具(F12)查看Console错误
2. 确认AntV Infographic库是否正确安装
3. 检查生成的配置数据格式

## 下一步

- 查看完整的 `README.md` 了解更多功能
- 访问 API文档探索所有接口: http://localhost:8000/api/v1/docs
- 尝试不同类型的文本,体验AI推荐效果
- 自定义Prompt提升AI生成质量

## 技术支持

如遇到问题,请检查:
1. Python版本 >= 3.11
2. Node.js版本 >= 18  
3. 所有依赖是否正确安装
4. 端口8000和5173是否被占用
