/**
 * 导出API
 */
import { apiClient } from './client'
import type { APIResponse } from './client'

/**
 * 导出请求参数
 */
export interface ExportRequest {
  svgContent: string
  format: 'svg' | 'png' | 'pdf' | 'pptx'
  filename?: string
  title?: string  // 仅PPTX
  width?: number  // 仅PNG
  height?: number  // 仅PNG
  scale?: number  // 仅PNG
}

/**
 * 导出响应
 */
export interface ExportResponse {
  format: string
  filename: string
  filepath: string
  size: number
  downloadUrl: string
  width?: number
  height?: number
}

/**
 * 导出格式
 */
export interface ExportFormat {
  value: string
  label: string
  description: string
  extension: string
}

/**
 * 导出信息图
 */
export async function exportInfographic(data: ExportRequest): Promise<APIResponse<ExportResponse>> {
  return apiClient.post('/export', data)
}

/**
 * 获取支持的导出格式
 */
export async function getExportFormats(): Promise<APIResponse<ExportFormat[]>> {
  return apiClient.get('/export/formats')
}

/**
 * 下载文件
 * 
 * @param filename 文件名
 * @returns 下载URL
 */
export function getDownloadUrl(filename: string): string {
  const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'
  return `${baseUrl}/export/download/${filename}`
}

/**
 * 清理临时文件
 */
export async function cleanupFile(filename: string): Promise<APIResponse<null>> {
  return apiClient.delete(`/export/cleanup/${filename}`)
}
