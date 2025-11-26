/**
 * 作品管理API
 */
import { apiClient } from './client'
import type { APIResponse } from './client'

/**
 * 作品创建请求
 */
export interface WorkCreateRequest {
  title: string
  templateId: string
  inputText: string
  infographicConfig: any
}

/**
 * 作品信息
 */
export interface Work {
  id: number
  title: string
  templateId: string
  inputText: string
  infographicConfig: any
  createdAt: string
  updatedAt: string
}

/**
 * 创建作品
 */
export async function createWork(data: WorkCreateRequest): Promise<APIResponse<Work>> {
  return apiClient.post('/works', data)
}

/**
 * 获取作品列表
 */
export async function getWorks(page = 1, pageSize = 20): Promise<APIResponse<{
  works: Work[]
  total: number
  page: number
  pageSize: number
}>> {
  return apiClient.get('/works', { params: { page, pageSize } })
}

/**
 * 获取单个作品
 */
export async function getWork(id: number): Promise<APIResponse<Work>> {
  return apiClient.get(`/works/${id}`)
}

/**
 * 删除作品
 */
export async function deleteWork(id: number): Promise<APIResponse<null>> {
  return apiClient.delete(`/works/${id}`)
}
