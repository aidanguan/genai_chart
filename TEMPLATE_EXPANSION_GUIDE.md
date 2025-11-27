# 模板扩展优化指南

## 📊 当前状态

- **现有模板数量**: 12个
- **目标模板数量**: 100+
- **AntV可用结构**: 30+ 种 structure 类型
- **覆盖率**: ~12%

---

## 🎯 优化策略

### 方案一：基于AntV现有结构快速扩展 ⭐推荐

**优势**: 
- ✅ 复用AntV官方已实现的30+种structure
- ✅ 无需开发新组件,配置即可用
- ✅ 稳定可靠,经过官方测试
- ✅ 可快速增加到50+模板

**可用结构清单** (基于 `/antv_infographic/infographic/esm/designs/structures/`):

#### 🔹 列表类 (List) - 6种结构
1. `list-row` - 横向列表
2. `list-column` - 纵向列表 ✅已用
3. `list-grid` - 网格列表
4. `list-pyramid` - 金字塔列表 ✅已用
5. `list-sector` - 扇形列表
6. `list-waterfall` - 瀑布流列表

#### 🔹 顺序类 (Sequence) - 13种结构
1. `sequence-steps` - 简单步骤
2. `sequence-zigzag-steps` - Z字形步骤 ✅已用
3. `sequence-horizontal-zigzag` - 横向Z字形
4. `sequence-timeline` - 时间轴
5. `sequence-circular` - 环形流程
6. `sequence-circle-arrows` - 圆形箭头流程
7. `sequence-ascending-steps` - 上升步骤
8. `sequence-ascending-stairs-3d` - 3D上升阶梯
9. `sequence-snake-steps` - 蛇形步骤
10. `sequence-color-snake-steps` - 彩色蛇形步骤
11. `sequence-mountain` - 山峰型流程
12. `sequence-pyramid` - 金字塔流程
13. `sequence-roadmap-vertical` - 垂直路线图
14. `sequence-cylinders-3d` - 3D圆柱体流程
15. `sequence-filter-mesh` - 过滤网格流程
16. `sequence-zigzag-pucks-3d` - 3D曲棍球流程

#### 🔹 对比类 (Comparison) - 3种结构
1. `compare-binary-horizontal` - 横向二元对比
2. `compare-hierarchy-left-right` - 左右层级对比
3. `compare-hierarchy-row` - 行层级对比

#### 🔹 层级类 (Hierarchy) - 1种结构
1. `hierarchy-tree` - 树形结构 (可配置多种样式)

#### 🔹 关系类 (Relation) - 2种结构
1. `relation-circle` - 圆形关系图
2. `relation-network` - 网络关系图

#### 🔹 图表类 (Chart) - 1种结构
1. `chart-column` - 柱状图 ✅已用

#### 🔹 四象限类 (Quadrant) - 1种结构
1. `quadrant` - 四象限图 ✅已用

---

## 🚀 快速扩展方案

### 第一步: 创建模板配置生成工具

创建 `backend/scripts/generate_templates_from_structures.py`:

```python
"""从AntV结构自动生成模板配置"""

STRUCTURE_TO_CATEGORY_MAP = {
    # 列表类
    'list-row': 'list',
    'list-column': 'list',
    'list-grid': 'list',
    'list-pyramid': 'hierarchy',
    'list-sector': 'list',
    'list-waterfall': 'list',
    
    # 顺序类
    'sequence-steps': 'sequence',
    'sequence-zigzag-steps': 'sequence',
    'sequence-horizontal-zigzag': 'sequence',
    'sequence-timeline': 'sequence',
    'sequence-circular': 'sequence',
    'sequence-circle-arrows': 'sequence',
    'sequence-ascending-steps': 'sequence',
    'sequence-ascending-stairs-3d': 'sequence',
    'sequence-snake-steps': 'sequence',
    'sequence-color-snake-steps': 'sequence',
    'sequence-mountain': 'sequence',
    'sequence-pyramid': 'sequence',
    'sequence-roadmap-vertical': 'sequence',
    'sequence-cylinders-3d': 'sequence',
    'sequence-filter-mesh': 'sequence',
    'sequence-zigzag-pucks-3d': 'sequence',
    
    # 对比类
    'compare-binary-horizontal': 'comparison',
    'compare-hierarchy-left-right': 'comparison',
    'compare-hierarchy-row': 'comparison',
    
    # 层级类
    'hierarchy-tree': 'hierarchy',
    
    # 关系类
    'relation-circle': 'relation',
    'relation-network': 'relation',
    
    # 图表类
    'chart-column': 'chart',
    
    # 四象限类
    'quadrant': 'quadrant',
}

TEMPLATE_METADATA = {
    'list-grid': {
        'name': '网格列表',
        'description': '网格布局展示多个项目,适合平铺展示',
        'use_cases': '产品展示、团队成员、功能特性、图标墙',
        'tags': ['网格', '列表', '平铺']
    },
    'list-sector': {
        'name': '扇形列表',
        'description': '扇形分布的列表布局,视觉效果独特',
        'use_cases': '服务介绍、产品分类、特性展示',
        'tags': ['扇形', '列表', '放射']
    },
    # ... 更多模板元数据
}
```

### 第二步: 批量生成模板JSON

运行工具自动生成50+模板的JSON配置:

```bash
python backend/scripts/generate_templates_from_structures.py
# 输出: backend/templates_expanded.json (50+个模板)
```

### 第三步: 导入到数据库

```bash
python backend/scripts/import_templates.py backend/templates_expanded.json
```

### 第四步: 更新Dify工作流配置

编辑 `backend/app/config/dify_workflows.yaml`,为新模板添加配置:

```yaml
# 新增模板
list-grid:
  dify_app_id: null
  workflow_name: "网格列表数据生成工作流"
  enabled: true
  fallback_to_system_llm: true

sequence-circular:
  dify_app_id: null
  workflow_name: "环形流程数据生成工作流"
  enabled: true
  fallback_to_system_llm: true
```

---

## 📋 模板扩展优先级建议

### 🔥 高优先级 (第一批: +20个)

**顺序类** (用户最常用):
- `sequence-circular` - 环形流程 (循环流程、生命周期)
- `sequence-ascending-steps` - 上升步骤 (进阶流程、成长路径)
- `sequence-roadmap-vertical` - 垂直路线图 (产品路线图、规划)
- `sequence-timeline` - 时间轴 (历史、里程碑)
- `sequence-snake-steps` - 蛇形步骤 (长流程)

**列表类** (通用性强):
- `list-grid` - 网格列表 (产品展示、团队)
- `list-sector` - 扇形列表 (服务、特性)
- `list-waterfall` - 瀑布流列表 (信息流)

**对比类** (决策场景):
- `compare-binary-horizontal` - 横向二元对比 (方案选择)
- `compare-hierarchy-left-right` - 左右层级对比 (复杂对比)

**关系类** (关联分析):
- `relation-circle` - 圆形关系图 (中心辐射)
- `relation-network` - 网络关系图 (复杂关系)

### ⚡ 中优先级 (第二批: +15个)

**顺序类高级**:
- `sequence-horizontal-zigzag` - 横向Z字形
- `sequence-mountain` - 山峰型流程
- `sequence-pyramid` - 金字塔流程
- `sequence-color-snake-steps` - 彩色蛇形步骤

**层级类**:
- `hierarchy-tree` + 多种item组合 (至少5种变体)

**3D视觉增强**:
- `sequence-ascending-stairs-3d` - 3D上升阶梯
- `sequence-cylinders-3d` - 3D圆柱体流程

### 🎨 低优先级 (第三批: +15个)

复杂视觉效果:
- `sequence-filter-mesh` - 过滤网格流程
- `sequence-zigzag-pucks-3d` - 3D曲棍球流程
- `sequence-circle-arrows` - 圆形箭头流程

---

## 🛠️ 数据Schema设计原则

### 通用字段
所有模板都应包含:
```json
{
  "title": {"type": "string", "required": false},
  "desc": {"type": "string", "required": false}
}
```

### 列表型 Schema
```json
{
  "items": {
    "type": "array",
    "required": true,
    "itemSchema": {
      "label": {"type": "string", "required": true},
      "desc": {"type": "string", "required": false},
      "value": {"type": "number", "required": false},
      "icon": {"type": "string", "required": false}
    }
  }
}
```

### 顺序型 Schema
```json
{
  "items": {
    "type": "array",
    "required": true,
    "itemSchema": {
      "label": {"type": "string", "required": true},
      "desc": {"type": "string", "required": false},
      "time": {"type": "string", "required": false}
    }
  }
}
```

### 对比型 Schema
```json
{
  "left": {
    "type": "object",
    "required": true,
    "schema": {
      "title": {"type": "string", "required": true},
      "items": {"type": "array", "required": true}
    }
  },
  "right": {
    "type": "object",
    "required": true,
    "schema": {
      "title": {"type": "string", "required": true},
      "items": {"type": "array", "required": true}
    }
  }
}
```

---

## 📦 自动化脚本开发计划

### 脚本1: 结构发现工具
```bash
python backend/scripts/discover_antv_structures.py
# 输出: 所有可用structure及其参数
```

### 脚本2: 模板配置生成器
```bash
python backend/scripts/generate_template_configs.py \
  --structures sequence-circular,list-grid,relation-circle \
  --output templates_batch1.json
```

### 脚本3: 批量测试工具
```bash
python backend/scripts/test_templates_batch.py \
  --template-file templates_batch1.json
# 自动测试每个模板的渲染
```

---

## 🎯 实施时间线

### Week 1: 基础设施 (已完成 ✅)
- [x] 数据库模型
- [x] 模板导入脚本
- [x] Dify集成

### Week 2: 第一批扩展 (+20个模板)
- [ ] 开发自动化生成脚本
- [ ] 生成高优先级模板配置
- [ ] 导入数据库
- [ ] 测试验证

### Week 3: 第二批扩展 (+15个模板)
- [ ] 生成中优先级模板配置
- [ ] 配置Dify工作流
- [ ] 前端UI适配

### Week 4: 第三批扩展 (+15个模板)
- [ ] 生成低优先级模板配置
- [ ] 全面测试
- [ ] 文档完善

### 最终目标: 60+模板 (5倍增长)

---

## 💡 进一步优化建议

### 1. 智能推荐优化
- 为新增模板补充关键词
- 优化LLM提示词,覆盖更多场景
- 建立模板相似度矩阵

### 2. 预览图生成
- 自动为每个模板生成预览图
- 使用示例数据渲染
- 存储到CDN

### 3. 模板评分系统
- 跟踪模板使用频率
- 用户反馈机制
- 动态调整推荐权重

### 4. 分阶段启用Dify
- 第一批: 仅System LLM (快速上线)
- 第二批: 高频模板启用Dify
- 第三批: 全量启用

---

## 🔗 相关资源

- [AntV Infographic官方文档](https://infographic.antv.vision/)
- [内置结构参考](https://infographic.antv.vision/reference/built-in-structures)
- [自定义结构指南](https://infographic.antv.vision/learn/custom-structure)
- [结构开发AI提示词](https://github.com/antvis/Infographic/blob/dev/src/designs/structures/prompt.md)

---

## ✅ 下一步行动

1. **立即执行**: 创建 `generate_templates_from_structures.py` 脚本
2. **本周完成**: 生成并导入第一批20个模板
3. **持续优化**: 根据用户反馈调整模板库
