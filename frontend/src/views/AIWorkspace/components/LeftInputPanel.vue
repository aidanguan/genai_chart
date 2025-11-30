<template>
  <div class="left-input-panel">
    <!-- 面板头部 -->
    <div class="panel-header">
      <div class="header-title">
        <FileText :size="18" class="title-icon" />
        <span class="title-text">输入内容</span>
      </div>
      <button 
        class="clear-btn" 
        @click="handleClear"
        :disabled="!hasInput"
        title="清空内容"
      >
        <Eraser :size="16" />
      </button>
    </div>

    <!-- 文本输入区域 -->
    <div class="panel-body">
      <textarea
        v-model="inputText"
        class="input-textarea"
        :placeholder="placeholder"
        :maxlength="5000"
      />
      
      <!-- 浮动操作按钮组 -->
      <div class="action-container">
        <button
          class="mode-btn smart-btn"
          @click="handleSmartGenerate"
          :disabled="isAnalyzing || !hasValidInput"
        >
          <template v-if="isAnalyzing">
            <div class="loading-spinner"></div>
            <span>生成中...</span>
          </template>
          <template v-else>
            <Sparkles :size="18" />
            <span>智能生成</span>
          </template>
        </button>
        
        <button
          class="mode-btn manual-btn"
          @click="handleManualSelect"
          :disabled="isAnalyzing || !hasValidInput"
        >
          <FileStack :size="18" />
          <span>手工选择</span>
        </button>
      </div>
    </div>
    
    <!-- 模板选择弹窗 -->
    <TemplateSelectionModal v-model="showTemplateModal" />
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { FileText, Sparkles, Eraser, FileStack } from 'lucide-vue-next'
import { message } from 'ant-design-vue'
import { useWorkspaceStore } from '@/stores/workspace'
import { useTemplateStore } from '@/stores/template'
import { useSettingsStore } from '@/stores/settings'
import TemplateSelectionModal from './TemplateSelectionModal.vue'

const workspaceStore = useWorkspaceStore()
const templateStore = useTemplateStore()
const settingsStore = useSettingsStore()

// 显示模板选择弹窗
const showTemplateModal = ref(false)

const placeholder = `输入您想要的可视化内容,可以是步骤说明、对比分析、组织架构等。AI会自动分析并推荐最合适的信息图模板。

例如:
这里有一个四个阶段的产品开发流程。第一阶段是概念验证,通过率10%;第二阶段是原型开发,通过率30%;第三阶段是市场测试...`

// 计算属性
const inputText = computed({
  get: () => workspaceStore.inputText,
  set: (value) => workspaceStore.setInputText(value)
})

const hasInput = computed(() => workspaceStore.hasInput)

const hasValidInput = computed(() => {
  const text = inputText.value.trim()
  return text.length >= 10 && text.length <= 5000
})

const isAnalyzing = computed(() => workspaceStore.isAnalyzing)

async function handleSmartGenerate() {
  if (!hasValidInput.value) {
    message.warning('请输入至少10个字的内容')
    return
  }
  
  try {
    workspaceStore.setAnalyzing(true)
    workspaceStore.setGenerationMode('smart')
    
    // 调用智能生成API，请求返回所有模板
    const generateModule = await import('@/api/generate')
    const response = await generateModule.generateAPI.smartGenerate(inputText.value, true)
    
    console.log('[LeftInputPanel] 智能生成响应:', response)
    
    if (response.success && response.data) {
      const { config, classification, selection, allTemplates } = response.data
      
      console.log('[LeftInputPanel] 分类:', classification)
      console.log('[LeftInputPanel] 选择:', selection)
      console.log('[LeftInputPanel] 配置:', config)
      console.log('[LeftInputPanel] 所有模板:', allTemplates)
      
      // 更新store
      workspaceStore.setSelectedTemplate(selection.templateId)
      workspaceStore.setConfig(config)
      workspaceStore.cacheTemplateConfig(selection.templateId, config)
      
      // 设置所有模板列表
      if (allTemplates && allTemplates.length > 0) {
        workspaceStore.setAllTemplates(allTemplates)
      }
      
      message.success(`分析完成！识别为${classification.type}类型，推荐使用${selection.templateName || selection.templateId}`)
    } else {
      message.warning('未找到合适的模板，请尝试调整输入内容')
    }
  } catch (error: any) {
    console.error('分析失败:', error)
    message.error(error.message || '分析失败，请稍后重试')
  } finally {
    workspaceStore.setAnalyzing(false)
  }
}

function handleManualSelect() {
  if (!hasValidInput.value) {
    message.warning('请输入至少10个字的内容')
    return
  }
  
  workspaceStore.setGenerationMode('manual')
  showTemplateModal.value = true
}

async function handleGenerate(templateId: string) {
  try {
    workspaceStore.setGenerating(true)
    
    // 调用数据提取API，传入LLM提供商配置
    const generateModule = await import('@/api/generate')
    const response = await generateModule.generateAPI.extractData(
      inputText.value,
      templateId,
      settingsStore.llmProvider  // 传入用户选择的LLM提供商
    )
    
    console.log('[LeftInputPanel] 数据提取响应:', response)
    
    if (response.success && response.data) {
      console.log('[LeftInputPanel] 设置config:', response.data.config)
      workspaceStore.setConfig(response.data.config)
      
      // 显示使用的LLM提供商
      const providerName = settingsStore.llmProvider === 'dify' ? 'Dify工作流' : '系统LLM'
      message.success(`信息图生成成功！(使用${providerName})`)
    } else {
      message.error('生成失败')
    }
  } catch (error: any) {
    console.error('生成失败:', error)
    message.error(error.message || '生成失败，请稍后重试')
  } finally {
    workspaceStore.setGenerating(false)
  }
}

function handleClear() {
  workspaceStore.reset()
  message.info('已清空内容')
}
</script>

<style scoped lang="scss">
.left-input-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  border: 1px solid #f0f0f0;
  overflow: hidden;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 4px 6px;
  border-bottom: 1px solid #f0f0f0;
  flex-shrink: 0;
  background: #fff;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #1f2937;
  font-weight: 600;
  font-size: 14px;
}

.title-icon {
  color: #3b82f6;
}

.clear-btn {
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  border-radius: 50%;
  color: #9ca3af;
  cursor: pointer;
  transition: all 0.2s;
  
  &:hover:not(:disabled) {
    background: #f3f4f6;
    color: #6b7280;
  }
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}

.panel-body {
  flex: 1;
  padding: 4px;
  position: relative;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}

.input-textarea {
  width: 100%;
  height: 100%;
  resize: none;
  outline: none;
  border: none;
  color: #4b5563;
  line-height: 1.6;
  font-size: 14px;
  background: transparent;
  padding: 8px;
  
  &::placeholder {
    color: #d1d5db;
  }
  
  &:focus {
    outline: none;
  }
}

.action-container {
  position: absolute;
  bottom: 24px;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  gap: 12px;
  padding: 0 24px;
  pointer-events: none;
}

.mode-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: 9999px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  color: white;
  font-weight: 500;
  transition: all 0.3s;
  border: none;
  cursor: pointer;
  pointer-events: auto;
  flex: 1;
  max-width: 180px;
  justify-content: center;
  
  &:hover:not(:disabled) {
    transform: scale(1.05);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  }
  
  &:active:not(:disabled) {
    transform: scale(0.95);
  }
  
  &:disabled {
    background: #d1d5db;
    cursor: not-allowed;
    transform: none;
  }
}

.smart-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
}

.manual-btn {
  background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid white;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
