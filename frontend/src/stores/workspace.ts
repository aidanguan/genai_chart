/**
 * 工作区状态管理
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface InfographicConfig {
  template?: string
  design?: any
  data: any
  themeConfig?: any
}

export const useWorkspaceStore = defineStore('workspace', () => {
  // 状态
  const inputText = ref('')
  const selectedTemplateId = ref<string | null>(null)
  const infographicConfig = ref<InfographicConfig | null>(null)
  const isAnalyzing = ref(false)
  const isGenerating = ref(false)
  
  // 计算属性
  const hasInput = computed(() => inputText.value.trim().length > 0)
  const hasConfig = computed(() => infographicConfig.value !== null)
  
  // 操作
  function setInputText(text: string) {
    inputText.value = text
  }
  
  function setSelectedTemplate(templateId: string) {
    selectedTemplateId.value = templateId
  }
  
  function setConfig(config: InfographicConfig) {
    infographicConfig.value = config
  }
  
  function setAnalyzing(analyzing: boolean) {
    isAnalyzing.value = analyzing
  }
  
  function setGenerating(generating: boolean) {
    isGenerating.value = generating
  }
  
  function reset() {
    inputText.value = ''
    selectedTemplateId.value = null
    infographicConfig.value = null
    isAnalyzing.value = false
    isGenerating.value = false
  }
  
  return {
    // 状态
    inputText,
    selectedTemplateId,
    infographicConfig,
    isAnalyzing,
    isGenerating,
    // 计算属性
    hasInput,
    hasConfig,
    // 操作
    setInputText,
    setSelectedTemplate,
    setConfig,
    setAnalyzing,
    setGenerating,
    reset
  }
})
