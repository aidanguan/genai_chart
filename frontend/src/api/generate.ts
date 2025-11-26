/**
 * 生成相关API
 */
import { apiClient } from './client'

export const generateAPI = {
  /**
   * 提取结构化数据
   */
  async extractData(text: string, templateId: string): Promise<any> {
    return apiClient.post('/generate/extract', { text, templateId })
  }
}
