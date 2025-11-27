# 导出功能依赖安装指南

## 概述

导出功能支持4种格式：
- **SVG**: 矢量图形，无需额外依赖
- **PNG**: 需要cairosvg库
- **PDF**: 需要cairosvg库
- **PPTX**: 需要python-pptx和cairosvg库

## 安装依赖

### 1. 基础依赖（SVG导出）

SVG导出不需要额外依赖，开箱即用。

### 2. PNG/PDF导出依赖

PNG和PDF导出需要cairosvg库，该库依赖Cairo图形库。

#### Windows安装

```bash
# 1. 下载并安装GTK+ for Windows (包含Cairo)
# 下载地址: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
# 选择最新版本的安装程序并安装

# 2. 安装Python包
pip install cairosvg
```

#### Linux (Ubuntu/Debian)安装

```bash
# 安装系统依赖
sudo apt-get update
sudo apt-get install libcairo2-dev pkg-config python3-dev

# 安装Python包
pip install cairosvg
```

#### macOS安装

```bash
# 使用Homebrew安装Cairo
brew install cairo pkg-config

# 安装Python包
pip install cairosvg
```

### 3. PPTX导出依赖

PPTX导出需要python-pptx库（用于生成PowerPoint文件）和cairosvg（用于SVG转PNG）。

```bash
# 先按照上述步骤安装cairosvg
# 然后安装python-pptx
pip install python-pptx
```

### 4. 一键安装所有依赖

```bash
# 安装所有导出功能依赖（需要先安装系统依赖Cairo）
pip install cairosvg python-pptx
```

## 功能降级

如果无法安装某些依赖，系统会优雅降级：

- 未安装cairosvg时，PNG/PDF/PPTX导出会返回友好错误提示
- SVG导出始终可用，不受影响
- 前端会显示相应的错误信息，引导用户使用可用的导出格式

## 验证安装

运行以下命令验证依赖是否正确安装：

```bash
python -c "import cairosvg; print('cairosvg: OK')"
python -c "import pptx; print('python-pptx: OK')"
```

## 故障排除

### 问题1: Windows上找不到Cairo

**解决方案**:
1. 确保已安装GTK+ for Windows
2. 将GTK的bin目录添加到系统PATH环境变量
3. 重启终端/IDE

### 问题2: Linux上编译失败

**解决方案**:
```bash
# 安装完整的开发工具链
sudo apt-get install build-essential libcairo2-dev libpango1.0-dev
```

### 问题3: macOS上找不到pkg-config

**解决方案**:
```bash
# 安装pkg-config
brew install pkg-config
```

## 性能优化建议

- PNG导出时，`scale`参数控制清晰度，建议值为2-3
- PPTX导出会先转换为高清PNG，可能需要几秒时间
- 大型信息图建议使用SVG格式，文件更小且支持无限缩放

## API使用示例

### 前端调用示例

```typescript
import { exportInfographic } from '@/api/export'

// 导出PNG
const response = await exportInfographic({
  svgContent: svgString,
  format: 'png',
  width: 1200,
  height: 800,
  scale: 2
})

// 导出PPTX
const response = await exportInfographic({
  svgContent: svgString,
  format: 'pptx',
  title: '我的信息图'
})
```

### 后端API端点

```
POST /api/v1/export
GET  /api/v1/export/download/{filename}
GET  /api/v1/export/formats
DELETE /api/v1/export/cleanup/{filename}
```

## 临时文件管理

- 导出的文件存储在 `backend/temp/exports/` 目录
- 建议定期清理临时文件
- 可以通过cleanup API删除不需要的文件

## 更多信息

- cairosvg文档: https://cairosvg.org/
- python-pptx文档: https://python-pptx.readthedocs.io/
