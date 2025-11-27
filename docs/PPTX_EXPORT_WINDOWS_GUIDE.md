# Windows 系统 PPTX 导出配置指南

## 问题说明

在 Windows 系统上导出 PPTX 格式时出现错误：
```
OSError: no library called "cairo-2" was found
cannot load library 'libcairo-2.dll': error 0x7e
```

**原因**：`cairosvg` Python 包依赖底层的 Cairo 图形库，该库在 Windows 上需要单独安装 DLL 文件。

---

## 当前可用的导出格式

✅ **PNG 格式**（前端直接导出，无需后端）
- 高清位图
- 支持自定义 DPI（默认 2x）
- **立即可用**

✅ **SVG 格式**（前端直接导出，无需后端）
- 矢量图形，可无限缩放
- 文件小，质量高
- **立即可用**

❌ **PPTX 格式**（需要 Cairo 库）
- 需要额外配置
- 请参考下方安装指南

---

## 方案一：安装 GTK+ Runtime（推荐）

### 步骤 1：下载 GTK+ Runtime

访问以下网址下载 GTK+ for Windows：
- **官方下载**：https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
- 下载最新版本的 `gtk3-runtime-x.x.x-x-x-x-ts-win64.exe`

### 步骤 2：安装 GTK+ Runtime

1. 运行下载的安装程序
2. 使用默认安装路径（通常是 `C:\Program Files\GTK3-Runtime Win64`）
3. **重要**：勾选 "Add to PATH" 选项
4. 完成安装

### 步骤 3：重启终端

关闭所有 PowerShell/CMD 窗口并重新打开，使 PATH 生效。

### 步骤 4：验证安装

```powershell
# 测试 Cairo 库是否可用
cd c:\AI\genai_chart-1\backend
python -c "import cairocffi; print('Cairo 库安装成功!')"
```

### 步骤 5：重启服务

```powershell
# 重启后端服务
cd c:\AI\genai_chart-1\backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 方案二：使用 Conda 环境

如果您使用 Anaconda/Miniconda：

```bash
conda install -c conda-forge cairo
conda install -c conda-forge pango
```

---

## 方案三：手动下载 DLL 文件（高级用户）

1. 从 https://github.com/preshing/cairo-windows/releases 下载预编译的 Cairo DLL
2. 将以下文件复制到 Python 的 `Scripts` 目录：
   - `libcairo-2.dll`
   - `libpng16-16.dll`
   - `zlib1.dll`
   - `libfreetype-6.dll`
   - `libfontconfig-1.dll`
3. 或者添加 DLL 所在目录到系统 PATH

---

## 替代方案：使用 Docker（推荐用于生产环境）

创建 `Dockerfile`：

```dockerfile
FROM python:3.11-slim

# 安装 Cairo 和相关依赖
RUN apt-get update && apt-get install -y \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install -r requirements.txt

# 复制应用代码
COPY . /app
WORKDIR /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 验证 PPTX 导出功能

安装完成后，测试导出功能：

```powershell
cd c:\AI\genai_chart-1\backend
python test_pptx_export.py
```

测试脚本内容（`test_pptx_export.py`）：

```python
from app.services.export_service import get_export_service

svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
  <circle cx="50" cy="50" r="40" fill="blue"/>
</svg>'''

try:
    service = get_export_service()
    result = service.export_pptx(svg_content, title="测试", filename="test.pptx")
    print(f"✅ PPTX 导出成功: {result}")
except Exception as e:
    print(f"❌ PPTX 导出失败: {e}")
```

---

## 故障排除

### 问题：找不到 libcairo-2.dll

**解决方法**：
1. 确认 GTK+ Runtime 已正确安装
2. 检查系统 PATH 是否包含 GTK+ 的 bin 目录
3. 重启计算机

### 问题：导入 cairosvg 时报错

**解决方法**：
```powershell
pip uninstall cairosvg cairocffi
pip install --no-cache-dir cairosvg cairocffi
```

---

## 当前状态

✅ PNG/SVG 导出 - **正常工作**
❌ PPTX 导出 - **需要安装 Cairo 库**

按照上述任一方案安装后，PPTX 导出功能即可使用。

---

## 技术支持

如果遇到问题，可以：
1. 查看后端日志（Terminal ID 1）
2. 查看浏览器控制台（F12 → Console）
3. 检查错误信息并参考本文档

建议：**优先使用 PNG/SVG 格式**，它们的质量足够高且无需额外配置。
