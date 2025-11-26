/**
 * 模板状态管理
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getTemplates, getCategories, recommendTemplates } from '@/api/templates'

export interface Template {
  id: string
  name: string
  category: string
  description?: string
  useCases?: string
  previewUrl?: string
  tags?: string[]
  dataSchema: any
  designConfig: any
}

export interface Category {
  code: string
  name: string
  description: string
  count: number
}

export interface TemplateRecommendation {
  templateId: string
  templateName: string
  confidence: number
  matchScore: number  // 为confidence的百分比形式
  reason: string
  category?: string
}

export const useTemplateStore = defineStore('template', () => {
  // 状态
  const templates = ref<Template[]>([])
  const categories = ref<Category[]>([])
  const recommendations = ref<TemplateRecommendation[]>([])
  const loading = ref(false)
  
  // 操作
  async function fetchTemplates(category?: string, keyword?: string) {
    loading.value = true
    try {
      const response = await getTemplates({ category, keyword, page: 1, pageSize: 100 })
      if (response.success && response.data) {
        templates.value = response.data.templates
      }
    } finally {
      loading.value = false
    }
  }
  
  async function fetchCategories() {
    try {
      const response = await getCategories()
      if (response.success && response.data) {
        categories.value = response.data
      }
    } catch (error) {
      console.error('获取分类失败:', error)
    }
  }
  
  async function fetchRecommendations(text: string, maxRecommendations = 5) {
    loading.value = true
    try {
      const response = await recommendTemplates({ text, maxRecommendations })
      if (response.success && response.data) {
        // 转换confidence为matchScore(百分比)
        const recs = response.data.recommendations.map((rec: any) => ({
          ...rec,
          matchScore: Math.round(rec.confidence * 100)
        }))
        recommendations.value = recs
        return { ...response.data, recommendations: recs }
      }
    } finally {
      loading.value = false
    }
  }
  
  function getTemplateById(id: string): Template | undefined {
    return templates.value.find(t => t.id === id)
  }
  
  return {
    // 状态
    templates,
    categories,
    recommendations,
    loading,
    // 操作
    fetchTemplates,
    fetchCategories,
    fetchRecommendations,
    getTemplateById
  }
})
