/**
 * 信息图Store
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { generateAPI } from '@/api/generate'

export const useInfographicStore = defineStore('infographic', () => {
  const currentConfig = ref<any>(null)
  const currentSVG = ref<string>('')
  const userInputText = ref<string>('')
  const loading = ref(false)
  const error = ref<string | null>(null)

  /**
   * 设置用户输入文本
   */
  function setUserInputText(text: string) {
    userInputText.value = text
  }

  /**
   * 生成信息图配置
   */
  async function generateConfig(text: string, templateId: string) {
    loading.value = true
    error.value = null
    try {
      const response = await generateAPI.extractData(text, templateId)
      if (response.success) {
        currentConfig.value = response.data.config
        return response.data.config
      }
    } catch (e: any) {
      error.value = e.message || '生成配置失败'
      throw e
    } finally {
      loading.value = false
    }
  }

  /**
   * 设置SVG内容
   */
  function setSVGContent(svg: string) {
    currentSVG.value = svg
  }

  /**
   * 清空状态
   */
  function reset() {
    currentConfig.value = null
    currentSVG.value = ''
    userInputText.value = ''
    error.value = null
  }

  return {
    currentConfig,
    currentSVG,
    userInputText,
    loading,
    error,
    setUserInputText,
    generateConfig,
    setSVGContent,
    reset
  }
})
