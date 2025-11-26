<template>
  <div class="left-input-panel">
    <div class="panel-header">
      <h2 class="panel-title">输入内容</h2>
      <span class="char-count">{{ charCount }} 字</span>
    </div>
    
    <div class="panel-body">
      <a-textarea
        v-model:value="inputText"
        :placeholder="placeholder"
        :rows="12"
        :maxlength="5000"
        show-count
        class="input-textarea"
        @input="onInputChange"
      />
      
      <div class="tips">
        <a-alert
          message="使用提示"
          description="输入您想要可视化的内容，可以是步骤说明、对比分析、组织架构等。AI会自动分析并推荐最合适的信息图模板。"
          type="info"
          show-icon
          closable
        />
      </div>
    </div>
    
    <div class="panel-footer">
      <a-space>
        <a-button
          type="primary"
          size="large"
          :loading="isAnalyzing"
          :disabled="!hasValidInput"
          @click="handleAnalyze"
        >
          <template #icon>
            <ThunderboltOutlined />
          </template>
          分析并推荐模板
        </a-button>
        
        <a-button
          size="large"
          :disabled="!hasInput"
          @click="handleClear"
        >
          清空
        </a-button>
      </a-space>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ThunderboltOutlined } from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import { useWorkspaceStore } from '@/stores/workspace'
import { useTemplateStore } from '@/stores/template'

const workspaceStore = useWorkspaceStore()
const templateStore = useTemplateStore()

const placeholder = `请输入您想要可视化的内容，例如：

1. 步骤说明：产品开发流程的5个关键步骤
2. 对比分析：两个方案的优劣势对比
3. 组织架构：公司的部门组织结构
4. 时间线：项目的发展历程
5. 数据展示：各部门的销售数据

建议输入100-500字，内容越详细，AI推荐越准确。`

// 计算属性
const inputText = computed({
  get: () => workspaceStore.inputText,
  set: (value) => workspaceStore.setInputText(value)
})

const charCount = computed(() => inputText.value.length)

const hasInput = computed(() => workspaceStore.hasInput)

const hasValidInput = computed(() => {
  const text = inputText.value.trim()
  return text.length >= 10 && text.length <= 5000
})

const isAnalyzing = computed(() => workspaceStore.isAnalyzing)

// 方法
function onInputChange() {
  // 输入改变时的处理
}

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
    
    // 调用数据提取API
    const generateModule = await import('@/api/generate')
    const response = await generateModule.generateAPI.extractData(
      inputText.value,
      templateId
    )
    
    console.log('[LeftInputPanel] 数据提取响应:', response)
    
    if (response.success && response.data) {
      console.log('[LeftInputPanel] 设置config:', response.data.config)
      workspaceStore.setConfig(response.data.config)
      message.success('信息图生成成功！')
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
  padding: 16px;
  overflow: hidden;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  flex-shrink: 0;
  background: #fff;
  padding-bottom: 4px;
}

.panel-title {
  margin: 0;
  font-size: 16px;
  font-weight: 500;
  color: #262626;
}

.char-count {
  font-size: 12px;
  color: #8c8c8c;
  background: #fff;
  padding: 2px 6px;
  border-radius: 4px;
  position: relative;
  z-index: 10;
}

.panel-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
  overflow-y: auto;
  overflow-x: hidden;
  min-height: 0;
  padding-bottom: 8px;
}

.input-textarea {
  resize: none;
  font-size: 14px;
  line-height: 1.6;
  flex: 1;
  min-height: 300px;
  
  :deep(.ant-input) {
    height: 100% !important;
    overflow-y: auto !important;
  }
}

.tips {
  flex-shrink: 0;
}

.panel-footer {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
  flex-shrink: 0;
}
</style>
