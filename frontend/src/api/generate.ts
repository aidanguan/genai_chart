/**
 * 生成相关API
 */
import { apiClient } from './client'
import type { LLMProvider } from '@/stores/settings'

export const generateAPI = {
  /**
   * 智能生成信息图（三阶段流程）
   */
  async smartGenerate(text: string): Promise<any> {
    return apiClient.post('/generate/smart', { text })
  },

  /**
   * 提取结构化数据（指定模板）
   */
  async extractData(text: string, templateId: string, llmProvider?: LLMProvider): Promise<any> {
    return apiClient.post('/generate/extract', { 
      text, 
      templateId,
      ...(llmProvider && { llmProvider })
    })
  }
}
