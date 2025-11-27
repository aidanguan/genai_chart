/**
 * 生成相关API
 */
import { apiClient } from './client'
import type { LLMProvider } from '@/stores/settings'

export const generateAPI = {
  /**
   * 提取结构化数据
   */
  async extractData(text: string, templateId: string, llmProvider?: LLMProvider): Promise<any> {
    return apiClient.post('/generate/extract', { 
      text, 
      templateId,
      ...(llmProvider && { llmProvider })
    })
  }
}
