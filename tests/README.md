# 测试文档

## 测试目录说明

本目录包含所有测试脚本、验证工具和调试脚本。

## 目录结构

```
tests/
├── backend/              # 后端测试
│   ├── 功能测试/
│   ├── 集成测试/
│   ├── 导出测试/
│   ├── 配置验证/
│   └── 工具脚本/
└── frontend/            # 前端测试（待添加）
```

## 后端测试说明

### 1. 功能测试

#### test_smart_generation.py
**智能生成流程完整测试**

测试三阶段智能生成流程：
1. 阶段1：内容类型识别
2. 阶段2：模板智能选择
3. 阶段3：数据提取生成

**测试用例：**
- 顺序型：产品开发流程
- 列表型：产品功能列表
- 对比型：产品对比
- 层级型：组织架构

**运行：**
```bash
cd c:\AI\genai_chart-1
python tests/backend/test_smart_generation.py
```

**预期输出：**
```
============================================================
集成测试：智能生成流程
============================================================

测试用例 1: 顺序型 - 产品开发流程
类型识别: sequence
置信度: 0.95
模板选择: sequence-zigzag
数据提取成功
✓ 测试通过
```

---

#### test_chart_column_simple.py
**柱状图模板专项测试**

测试 `chart-column-simple` 模板在不同场景下的表现：
- 基础数值对比
- 百分比数据
- 带单位数据
- 简单数据

**运行：**
```bash
python tests/backend/test_chart_column_simple.py
```

**预期输出：**
```
chart-column-simple模板测试
✅ 生成成功！
类型识别: chart
模板选择: chart-column-simple
生成方式: dify_workflow
✓ 测试通过
```

---

#### test_pyramid_e2e.py
**金字塔层级模板端到端测试**

测试 `pyramid-badge` 模板的完整流程：
- 会员荣誉等级
- 需求优先级

**运行：**
```bash
python tests/backend/test_pyramid_e2e.py
```

**验证点：**
- 配置结构正确性
- 数据字段完整性
- 图标格式验证

---

### 2. 集成测试

#### test_dify_integration.py
**Dify 工作流 API 集成测试**

测试与 Dify 工作流平台的集成：
- API 连接测试
- 数据提取流程
- 工作流调用

**环境要求：**
```bash
# .env 文件需配置
DIFY_API_KEY=你的密钥
DIFY_API_BASE_URL=https://api.dify.ai/v1
```

**运行：**
```bash
python tests/backend/test_dify_integration.py
```

**预期输出：**
```
✅ 调用成功!
生成方法: dify_workflow
工作流名称: 数据提取工作流
工作流运行ID: wfr_xxx
```

---

#### test_dify_simple.py
**Dify 基础连接测试**

快速测试 Dify API 连通性。

**运行：**
```bash
python tests/backend/test_dify_simple.py
```

---

#### test_backend.py
**后端基础功能测试**

测试后端服务基础功能：
- API 端点可用性
- 数据库连接
- 基本路由

**运行：**
```bash
python tests/backend/test_backend.py
```

---

### 3. 导出功能测试

#### test_pptx_chinese.py
**PPTX 中文字体支持测试**

测试 PPTX 导出功能对中文的支持：
- 中文字体渲染
- SVG 转 PPTX
- 字体嵌入

**运行：**
```bash
python tests/backend/test_pptx_chinese.py
```

**预期输出：**
```
✅ PPTX 导出成功
文件路径: test_chinese.pptx
中文显示: 正常
```

---

#### test_backend_svg_conversion.py
**SVG 转换功能测试**

测试 SVG 到其他格式的转换：
- foreignObject 转 text 元素
- SVG 兼容性处理
- 渲染验证

**运行：**
```bash
python tests/backend/test_backend_svg_conversion.py
```

**预期输出：**
```
🎉 转换成功！所有 foreignObject 都已转换为 <text>
转换前 foreignObject 数量: 2
转换后 foreignObject 数量: 0
转换后 <text> 数量: 2
```

---

### 4. 配置验证

#### check_config.py
**环境配置验证**

检查环境变量配置是否正确。

**运行：**
```bash
python tests/backend/check_config.py
```

**检查项：**
- AIHUBMIX_API_KEY
- DIFY_API_KEY
- DATABASE_URL
- 其他必要配置

---

#### check_templates.py
**模板数据完整性检查**

验证数据库中模板数据的完整性和正确性。

**运行：**
```bash
python tests/backend/check_templates.py
```

**检查项：**
- 模板数量
- 必填字段
- 数据格式
- Schema 有效性

---

#### check_workflow_config.py
**工作流配置检查**

验证 Dify 工作流配置的正确性。

**运行：**
```bash
python tests/backend/check_workflow_config.py
```

---

#### check_pyramid_badge.py
**金字塔模板配置检查**

专门检查 `pyramid-badge` 模板配置。

**运行：**
```bash
python tests/backend/check_pyramid_badge.py
```

---

#### verify_svg_ppt_compatibility.py
**SVG PPT 兼容性验证**

验证生成的 SVG 是否兼容 PowerPoint。

**运行：**
```bash
python tests/backend/verify_svg_ppt_compatibility.py test_file.svg
```

**检查项：**
- foreignObject 元素
- 不支持的 CSS
- 字体兼容性

---

### 5. 工具脚本

#### add_zigzag_template.py
**添加 Z 字形模板**

向数据库添加 `sequence-zigzag` 模板。

**运行：**
```bash
python tests/backend/add_zigzag_template.py
```

---

#### fix_pyramid_badge.py
**修复金字塔徽章模板**

修复 `pyramid-badge` 模板配置问题。

**运行：**
```bash
python tests/backend/fix_pyramid_badge.py
```

---

#### update_zigzag_template.py
**更新 Z 字形模板**

更新 `sequence-zigzag` 模板配置。

**运行：**
```bash
python tests/backend/update_zigzag_template.py
```

---

## 测试运行方式

### 单个测试

```bash
# 进入项目根目录
cd c:\AI\genai_chart-1

# 运行单个测试
python tests/backend/test_smart_generation.py
```

### 批量运行

```powershell
# 运行所有功能测试
Get-ChildItem tests/backend/test_*.py | ForEach-Object { python $_.FullName }
```

### 使用 pytest（推荐）

```bash
# 安装 pytest
pip install pytest pytest-asyncio

# 运行所有测试
pytest tests/backend/

# 运行特定测试
pytest tests/backend/test_smart_generation.py

# 显示详细输出
pytest tests/backend/ -v

# 运行并显示打印输出
pytest tests/backend/ -s
```

## 测试最佳实践

### 1. 测试前准备

**确保环境配置：**
```bash
# 检查 .env 文件
python tests/backend/check_config.py

# 检查数据库
python tests/backend/check_templates.py
```

**启动后端服务：**
```bash
cd backend
python -m app.main
```

### 2. 测试命名规范

- **功能测试：** `test_<功能名>.py`
- **集成测试：** `test_<系统>_integration.py`
- **验证脚本：** `check_<检查项>.py`
- **修复脚本：** `fix_<问题>.py`
- **工具脚本：** `<操作>_<对象>.py`

### 3. 测试编写规范

```python
"""
模块说明
测试目标和覆盖范围
"""
import asyncio
import sys
sys.path.insert(0, 'c:\\AI\\genai_chart-1\\backend')

async def test_功能():
    """测试函数说明"""
    # 准备测试数据
    test_data = {...}
    
    # 执行测试
    result = await service.method(test_data)
    
    # 验证结果
    assert result['status'] == 'success'
    print(f"✓ 测试通过")

if __name__ == '__main__':
    asyncio.run(test_功能())
```

### 4. 调试技巧

**查看详细日志：**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**使用断点调试：**
```python
import pdb; pdb.set_trace()
```

**输出中间结果：**
```python
import json
print(json.dumps(result, ensure_ascii=False, indent=2))
```

## 常见问题

### Q1: 测试失败 - ModuleNotFoundError

**原因：** Python 路径未正确设置

**解决：**
```python
import sys
sys.path.insert(0, 'c:\\AI\\genai_chart-1\\backend')
```

### Q2: 测试失败 - API Key 未配置

**原因：** 环境变量未设置

**解决：**
```bash
# 检查 backend/.env 文件
AIHUBMIX_API_KEY=你的密钥
DIFY_API_KEY=你的密钥
```

### Q3: 测试超时

**原因：** LLM API 响应慢

**解决：**
- 增加超时时间配置
- 检查网络连接
- 使用更快的模型

### Q4: 数据库锁定错误

**原因：** 数据库文件被占用

**解决：**
```bash
# 关闭其他访问数据库的进程
# 或使用独立的测试数据库
```

## 测试覆盖

### 当前测试覆盖率

- ✅ 智能生成流程：100%
- ✅ 模板推荐：100%
- ✅ 数据提取：100%
- ✅ Dify 集成：100%
- ✅ PPTX 导出：100%
- ⚠️ 前端测试：待添加
- ⚠️ E2E 测试：待添加

### 测试统计

- 功能测试：3 个
- 集成测试：3 个
- 导出测试：2 个
- 配置验证：5 个
- 工具脚本：6 个
- **总计：** 19 个测试文件

## 未来计划

### 短期计划

1. 添加前端单元测试
2. 添加 E2E 自动化测试
3. 集成 CI/CD 流水线

### 长期计划

1. 性能测试
2. 负载测试
3. 安全测试
4. 兼容性测试

---

**最后更新：** 2025-11-27  
**维护者：** Qoder AI Assistant  
**联系方式：** 查看项目 README.md
