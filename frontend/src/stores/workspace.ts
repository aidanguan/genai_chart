/**
 * 工作区状态管理
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface TemplateWithSimilarity {
  templateId: string
  templateName: string
  category: string
  similarityScore: number
  reason: string
}

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
  
  // 新增状态：生成模式、模板列表、缓存
  const generationMode = ref<'smart' | 'manual'>('smart')
  const allTemplates = ref<TemplateWithSimilarity[]>([])
  const templateCache = ref<Map<string, InfographicConfig>>(new Map())
  
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
    generationMode.value = 'smart'
    allTemplates.value = []
    templateCache.value.clear()
  }
  
  // 新增方法
  function setGenerationMode(mode: 'smart' | 'manual') {
    generationMode.value = mode
  }
  
  function setAllTemplates(templates: TemplateWithSimilarity[]) {
    allTemplates.value = templates
  }
  
  function cacheTemplateConfig(templateId: string, config: InfographicConfig) {
    templateCache.value.set(templateId, config)
  }
  
  function getCachedConfig(templateId: string): InfographicConfig | undefined {
    return templateCache.value.get(templateId)
  }
  
  function clearTemplateCache(templateId: string) {
    templateCache.value.delete(templateId)
  }
  
  function clearAllCache() {
    templateCache.value.clear()
  }
  
  return {
    // 状态
    inputText,
    selectedTemplateId,
    infographicConfig,
    isAnalyzing,
    isGenerating,
    generationMode,
    allTemplates,
    templateCache,
    // 计算属性
    hasInput,
    hasConfig,
    // 操作
    setInputText,
    setSelectedTemplate,
    setConfig,
    setAnalyzing,
    setGenerating,
    setGenerationMode,
    setAllTemplates,
    cacheTemplateConfig,
    getCachedConfig,
    clearTemplateCache,
    clearAllCache,
    reset
  }
})
