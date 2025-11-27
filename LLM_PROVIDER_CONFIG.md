# 🎛️ LLM提供商配置功能

## 功能概述

为用户提供了在右上角菜单中选择LLM提供商的能力,支持在 **系统LLM** 和 **Dify工作流** 之间切换。

---

## 📍 用户界面

### 位置
**右上角用户菜单** → 点击用户头像展开下拉菜单

### 菜单选项

#### 1️⃣ 系统LLM (默认)
- **图标**: 💻 CPU
- **名称**: 系统LLM
- **描述**: 使用内置AI模型
- **适用场景**: 快速响应,稳定可靠

#### 2️⃣ Dify工作流
- **图标**: ⚙️ Workflow  
- **名称**: Dify工作流
- **描述**: 使用Dify平台处理
- **适用场景**: 复杂场景,专业定制

---

## 🔧 技术实现

### 前端实现

#### 1. 状态管理 (`stores/settings.ts`)
```typescript
export type LLMProvider = 'system' | 'dify'

export const useSettingsStore = defineStore('settings', () => {
  const llmProvider = ref<LLMProvider>('system')  // 默认系统LLM
  
  function setLLMProvider(provider: LLMProvider) {
    llmProvider.value = provider
  }
  
  return { llmProvider, setLLMProvider }
})
```

**功能**:
- 自动保存到 `localStorage`
- 刷新页面后保持选择
- 响应式状态更新

#### 2. 用户菜单组件 (`WorkspaceHeader.vue`)
```vue
<template>
  <div class="user-menu">
    <button @click="toggleMenu">
      <User /> 用户
    </button>
    
    <div v-if="isMenuOpen" class="dropdown-menu">
      <button @click="handleProviderChange('system')">
        <Cpu /> 系统LLM
      </button>
      <button @click="handleProviderChange('dify')">
        <Workflow /> Dify工作流
      </button>
    </div>
  </div>
</template>
```

#### 3. API调用更新 (`LeftInputPanel.vue`)
```typescript
import { useSettingsStore } from '@/stores/settings'

const settingsStore = useSettingsStore()

// 调用API时传入用户选择
const response = await generateAPI.extractData(
  inputText.value,
  templateId,
  settingsStore.llmProvider  // 传递用户配置
)
```

---

### 后端实现

#### 1. Schema更新 (`schemas/infographic.py`)
```python
from typing import Literal, Optional

class DataExtractRequest(BaseModel):
    text: str
    templateId: str
    llmProvider: Optional[Literal['system', 'dify']] = Field(
        default='system',
        description="LLM提供商: system(系统LLM) 或 dify(Dify工作流)"
    )
```

#### 2. API端点更新 (`api/v1/generate.py`)
```python
@router.post("/extract")
async def extract_data(request: DataExtractRequest):
    result = await generate_service.extract_data(
        user_text=request.text,
        template_id=request.templateId,
        force_provider=request.llmProvider  # 传递用户选择
    )
    return APIResponse(success=True, data=result)
```

#### 3. 服务逻辑增强 (`services/generate_service.py`)
```python
async def extract_data(
    self,
    user_text: str,
    template_id: str,
    force_provider: Optional[str] = None  # 新增参数
) -> Dict[str, Any]:
    """
    force_provider控制逻辑:
    - 'system': 强制使用系统LLM
    - 'dify': 强制使用Dify工作流
    - None: 自动选择(默认行为)
    """
    
    # 强制使用系统LLM
    if force_provider == 'system':
        return await self._extract_data_with_system_llm(...)
    
    # 强制使用Dify
    if force_provider == 'dify':
        return await self._extract_data_with_dify(...)
    
    # 自动选择(原有逻辑)
    if self.workflow_mapper.is_workflow_enabled(template_id):
        # 尝试Dify,失败回退到系统LLM
        ...
```

---

## 📊 配置优先级

### 决策流程
```
用户选择LLM提供商
     |
     ├─ 选择"系统LLM" → 强制使用系统LLM
     |
     ├─ 选择"Dify工作流" → 强制使用Dify
     |     |
     |     └─ Dify调用失败 → 抛出错误(不回退)
     |
     └─ 未选择(默认) → 自动选择
           |
           ├─ 模板配置启用Dify → 使用Dify
           |     |
           |     └─ Dify失败 → 回退到系统LLM
           |
           └─ 模板未配置Dify → 使用系统LLM
```

---

## 💡 使用场景

### 场景1: 快速测试
**选择**: 系统LLM  
**原因**: 无需配置Dify,响应快速

### 场景2: 生产环境
**选择**: Dify工作流  
**原因**: 专业定制,质量稳定

### 场景3: Dify配置测试
**选择**: 强制Dify  
**原因**: 验证工作流是否正常

### 场景4: Dify故障降级
**选择**: 系统LLM  
**原因**: Dify服务异常时的备选方案

---

## ✅ 核心特性

1. ✨ **用户友好**: 右上角菜单,一键切换
2. 💾 **持久化保存**: 配置保存在localStorage
3. 🔒 **强制模式**: 用户选择优先级最高
4. 🔄 **自动回退**: 仅在自动模式下回退
5. 📝 **清晰提示**: 生成成功后显示使用的提供商

---

## 🗂️ 修改文件清单

### 前端 (4个文件)
1. ✅ `frontend/src/stores/settings.ts` - 新增配置store
2. ✅ `frontend/src/views/AIWorkspace/components/WorkspaceHeader.vue` - 添加下拉菜单
3. ✅ `frontend/src/api/generate.ts` - API调用支持llmProvider参数
4. ✅ `frontend/src/views/AIWorkspace/components/LeftInputPanel.vue` - 传递用户配置

### 后端 (3个文件)
1. ✅ `backend/app/schemas/infographic.py` - 添加llmProvider字段
2. ✅ `backend/app/api/v1/generate.py` - 传递force_provider参数
3. ✅ `backend/app/services/generate_service.py` - 实现force_provider逻辑

---

## 🚀 使用示例

### 前端调用
```typescript
import { useSettingsStore } from '@/stores/settings'
import { generateAPI } from '@/api/generate'

const settingsStore = useSettingsStore()

// 用户通过右上角菜单选择了"Dify工作流"
// settingsStore.llmProvider = 'dify'

// 生成信息图时自动使用用户配置
const response = await generateAPI.extractData(
  '这是一个产品开发流程...',
  'sequence-steps',
  settingsStore.llmProvider  // 'dify'
)

// 响应: { success: true, data: { config: {...}, generation_method: 'dify_workflow' } }
```

### 后端日志
```
[ExtractData] 用户强制使用Dify工作流 - 模板: sequence-steps
[Dify] 调用工作流成功 - workflow_run_id: abc123
[ExtractData] 数据提取成功 - 耗时: 2.3s
```

---

## 📌 注意事项

1. **默认值**: 系统默认使用`system` (系统LLM)
2. **兼容性**: 旧版API调用(未传llmProvider)仍正常工作
3. **错误处理**: 强制使用Dify时失败会抛出错误,不自动回退
4. **配置持久化**: 用户选择保存在localStorage,跨会话保持
5. **提示信息**: 生成成功后会显示使用的提供商名称

---

## 🎉 完成!

用户现在可以通过右上角菜单自由切换LLM提供商,获得更灵活的使用体验!