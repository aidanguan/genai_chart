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
      
      <!-- 浮动操作按钮 -->
      <div class="action-container">
        <button
          class="analyze-btn"
          @click="handleAnalyze"
          :disabled="isAnalyzing || !hasValidInput"
        >
          <template v-if="isAnalyzing">
            <div class="loading-spinner"></div>
            <span>分析中...</span>
          </template>
          <template v-else>
            <Sparkles :size="18" />
            <span>分析并推荐模版</span>
          </template>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { FileText, Sparkles, Eraser } from 'lucide-vue-next'
import { message } from 'ant-design-vue'
import { useWorkspaceStore } from '@/stores/workspace'
import { useTemplateStore } from '@/stores/template'
import { useSettingsStore } from '@/stores/settings'

const workspaceStore = useWorkspaceStore()
const templateStore = useTemplateStore()
const settingsStore = useSettingsStore()

const placeholder = `输入您想要的可视化内容,可以是步骤说明、对比分析、组织架构等。AI会自动分析并推荐最合适的信息图模板。

例如:
这里有一个四个阶段的产品开发流程。第一阶段是概念验证,通过率 10%;第二阶段是原型开发,通过率 30%;第三阶段是市场测试...`

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

async function handleAnalyze() {
  if (!hasValidInput.value) {
    message.warning('请输入至少10个字的内容')
    return
  }
  
  try {
    workspaceStore.setAnalyzing(true)
    
    // 调用AI推荐
    const result = await templateStore.fetchRecommendations(inputText.value)
    
    if (result && result.recommendations && result.recommendations.length > 0) {
      message.success(`分析完成！为您推荐了 ${result.recommendations.length} 个模板`)
      
      // 自动选择第一个推荐的模板
      const firstTemplate = result.recommendations[0]
      workspaceStore.setSelectedTemplate(firstTemplate.templateId)
      
      // 自动生成信息图
      await handleGenerate(firstTemplate.templateId)
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
  padding: 16px;
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
  padding: 16px;
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
  padding: 0 24px;
  pointer-events: none;
}

.analyze-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border-radius: 9999px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  color: white;
  font-weight: 500;
  transition: all 0.3s;
  border: none;
  cursor: pointer;
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
  pointer-events: auto;
  
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
