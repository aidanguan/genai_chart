"""
Prompt模板工程
用于生成LLM的提示词
"""
import json
from typing import List, Dict, Any


def get_template_recommend_prompt(
    user_text: str,
    available_templates: List[Dict[str, Any]],
    max_recommendations: int = 5
) -> str:
    """
    生成模板推荐的Prompt
    
    Args:
        user_text: 用户输入文本
        available_templates: 可用模板列表
        max_recommendations: 最多推荐数量
    
    Returns:
        str: Prompt文本
    """
    templates_desc = []
    for tmpl in available_templates:
        desc = f"- ID: {tmpl['id']}\n  名称: {tmpl['name']}\n  分类: {tmpl.get('category', '未分类')}\n  描述: {tmpl.get('description', '暂无描述')}\n  适用场景: {tmpl.get('适用场景', '')}"
        templates_desc.append(desc)
    
    templates_text = "\n\n".join(templates_desc)
    
    prompt = f"""请分析以下用户输入的文本内容，并从可用模板列表中推荐最适合的{max_recommendations}个信息图模板。

用户输入文本：
\"\"\"
{user_text}
\"\"\"

可用模板列表：
{templates_text}

## 信息图7大分类体系：

### 1. 图表型 (chart)
- **特征**：包含数值数据、统计信息、量化指标
- **关键词**：数据、增长率、比例、百分比、趋势、统计、图表、指标
- **适用场景**：销售数据、用户增长、KPI指标、财务报表、市场分析
- **示例**："2023年Q1销售额1000万，Q2增长20%"

### 2. 对比型 (comparison)
- **特征**：两个或多个事物的对比、优劣分析、差异展示
- **关键词**：VS、对比、优劣势、差异、区别、选择、竞争、比较
- **适用场景**：产品对比、竞品分析、方案比较、优缺点对比
- **示例**："产品A与产品B的功能对比"

### 3. 层级型 (hierarchy)
- **特征**：具有上下级、父子关系、分级结构
- **关键词**：组织架构、层级、分类、体系、级别、树形、上下级
- **适用场景**：公司架构、产品分类、知识体系、职级体系
- **示例**："公司组织架构：CEO-部门经理-员工"

### 4. 列表型 (list)
- **特征**：并列的项目、要点、特性、步骤
- **关键词**：要点、步骤、特性、功能、特点、清单、列举
- **适用场景**：产品功能、解决方案、服务项目、特性列表
- **示例**："产品的五大功能：1.智能推荐 2.数据分析..."

### 5. 四象限型 (quadrant)
- **特征**：两个维度划分，四个区域
- **关键词**：矩阵、象限、维度、重要紧急、优先级、分类
- **适用场景**：时间管理矩阵、优先级分类、SWOT分析、风险矩阵
- **示例**："任务分为重要紧急、重要不紧急、不重要紧急、不重要不紧急"

### 6. 关系型 (relationship)
- **特征**：元素之间的关联、因果、依赖、影响
- **关键词**：关系、因果、影响、联系、相关、交互、依赖
- **适用场景**：因果分析、业务流程、系统架构、关系网络
- **示例**："用户增长影响因素：产品质量、营销投入、口碑传播"

### 7. 顺序型 (sequence)
- **特征**：有先后顺序、时间线、流程
- **关键词**：步骤、流程、过程、顺序、阶段、时间线、发展、历史
- **适用场景**：操作流程、项目进度、历史进程、用户旅程
- **示例**："产品开发流程：需求分析-设计-开发-测试-上线"

## 分析指南：

1. **识别内容类型**：
   - 检查文本中是否包含数值数据 → 图表型
   - 检查是否有对比性描述 → 对比型
   - 检查是否有层级结构 → 层级型
   - 检查是否是并列项目 → 列表型
   - 检查是否有两个维度 → 四象限型
   - 检查是否描述关系 → 关系型
   - 检查是否有时间/顺序 → 顺序型

2. **匹配模板**：
   - 根据内容类型匹配对应分类的模板
   - 考虑模板的适用场景和用户文本的区配度
   - 优先选择特征匹配度高的模板

3. **评估置信度**：
   - 0.9-1.0：非常匹配，内容特征与模板高度一致
   - 0.7-0.9：较好匹配，大部分特征符合
   - 0.5-0.7：可以使用，部分特征符合
   - <0.5：不推荐

4. **排序优先级**：
   - 按照置信度从高到低排序
   - 最多返回{max_recommendations}个推荐

请**必须以纯JSON格式返回**,不要包含任何markdown代码块标记(如```json),不要包含任何其他文字说明,直接返回JSON对象:

{{
  "recommendations": [
    {{
      "templateId": "模板ID",
      "templateName": "模板名称",
      "confidence": 0.95,
      "reason": "推荐理由，说明为什么这个模板适合用户的文本内容，结合分类特征说明",
      "category": "分类(如chart/comparison/hierarchy/list/quadrant/relationship/sequence)"
    }}
  ]
}}

注意：confidence是0-1之间的数值，表示推荐置信度。请确保返回有效的JSON格式。"""
    
    return prompt


def get_data_extract_prompt(
    user_text: str,
    template_id: str,
    template_schema: Dict[str, Any]
) -> str:
    """
    生成数据提取的Prompt
    
    Args:
        user_text: 用户输入文本
        template_id: 模板ID
        template_schema: 模板数据结构定义
    
    Returns:
        str: Prompt文本
    """
    schema_text = json.dumps(template_schema, ensure_ascii=False, indent=2)
    
    prompt = f"""请从以下用户输入的文本中提取关键信息，并按照指定的数据结构进行组织。

用户输入文本：
\"\"\"
{user_text}
\"\"\"

目标模板ID：{template_id}

要求的数据结构（JSON Schema）：
```json
{schema_text}
```

请按照以下步骤完成数据提取：

1. 仔细阅读用户文本，识别关键信息点
2. 根据数据结构要求，提取相应的字段内容
3. 如果文本中没有明确提到某些字段，可以根据上下文推断或使用合理的默认值
4. 对于items数组，提取所有关键数据项
5. 如果文本包含图标、颜色等视觉元素的描述，尽量在配置中体现

关键字段说明：
- title: 信息图的标题（如果文本没有明确标题，可以根据内容生成一个简洁的标题）
- desc: 信息图的描述或副标题
- items: 数据项列表，每个item包含label（标签）、desc（描述）、icon（图标）等字段
  * label: 简短的标题或名称
  * desc: 详细的描述内容
  * icon: **必须生成**图标字段，使用iconify格式"icon:mdi/图标名"（仅使用mdi集合），例如：
    - 需求分析: "icon:mdi/chart-line" 或 "icon:mdi/clipboard-text"
    - 设计: "icon:mdi/palette" 或 "icon:mdi/draw"
    - 开发: "icon:mdi/code-braces" 或 "icon:mdi/laptop"
    - 测试: "icon:mdi/test-tube" 或 "icon:mdi/bug"
    - 部署: "icon:mdi/rocket-launch" 或 "icon:mdi/cloud-upload"
    - 分析: "icon:mdi/magnify" 或 "icon:mdi/chart-bar"
    - 创新: "icon:mdi/lightbulb" 或 "icon:mdi/creation"
    请根据每个步骤的含义选择合适的mdi图标，可在 https://icon-sets.iconify.design/mdi/ 查找更多图标

请严格按照JSON格式返回提取的数据，**不要包含任何markdown代码块标记(如```json)**,不要包含任何其他文字说明,直接返回JSON对象:

{{
  "template": "{template_id}",
  "data": {{
    "title": "提取的标题",
    "desc": "提取的描述",
    "items": [
      {{
        "label": "项目标签",
        "desc": "项目描述",
        "icon": "icon:mdi/相关图标名"
      }}
    ]
  }},
  "themeConfig": {{
    "palette": "antv"
  }}
}}

注意：确保返回有效的JSON格式，数组中的每个对象都包含必需的字段。"""
    
    return prompt


# 预定义的模板示例Schema
TEMPLATE_SCHEMAS = {
    "list-row-simple-horizontal-arrow": {
        "description": "横向流程图，带箭头",
        "dataFields": {
            "title": {"type": "string", "required": False, "description": "标题"},
            "desc": {"type": "string", "required": False, "description": "描述"},
            "items": {
                "type": "array",
                "required": True,
                "description": "数据项列表",
                "itemSchema": {
                    "label": {"type": "string", "required": True, "description": "步骤标签"},
                    "desc": {"type": "string", "required": False, "description": "步骤描述"}
                }
            }
        }
    },
    "list-row-horizontal-icon-arrow": {
        "description": "横向流程图，带图标和箭头",
        "dataFields": {
            "title": {"type": "string", "required": False},
            "desc": {"type": "string", "required": False},
            "items": {
                "type": "array",
                "required": True,
                "itemSchema": {
                    "label": {"type": "string", "required": True},
                    "desc": {"type": "string", "required": False},
                    "icon": {"type": "string", "required": False, "description": "图标，格式：icon:mdi/iconname"}
                }
            }
        }
    }
}
