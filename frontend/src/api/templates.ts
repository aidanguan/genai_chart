/**
 * 模板相关API
 */
import { apiClient } from './client'

export interface Template {
  id: string
  name: string
  category: string
  description: string
  适用场景: string
}

export interface TemplateRecommendation {
  templateId: string
  templateName: string
  confidence: number
  reason: string
  category?: string
}

export const templateAPI = {
  /**
   * 获取模板列表
   */
  async getTemplates(params?: { category?: string; keyword?: string; page?: number; pageSize?: number }): Promise<any> {
    return apiClient.get('/templates', { params })
  },

  /**
   * 获取单个模板详情
   */
  async getTemplate(templateId: string): Promise<any> {
    return apiClient.get(`/templates/${templateId}`)
  },

  /**
   * 获取分类列表
   */
  async getCategories(): Promise<any> {
    return apiClient.get('/templates/categories')
  },

  /**
   * AI推荐模板
   */
  async recommendTemplates(params: { text: string; maxRecommendations?: number }): Promise<any> {
    return apiClient.post('/templates/recommend', { 
      text: params.text, 
      maxRecommendations: params.maxRecommendations || 5 
    })
  }
}

// 导出为单独函数（与store中的导入保持一致）
export const getTemplates = templateAPI.getTemplates
export const getTemplate = templateAPI.getTemplate
export const getCategories = templateAPI.getCategories
export const recommendTemplates = templateAPI.recommendTemplates
