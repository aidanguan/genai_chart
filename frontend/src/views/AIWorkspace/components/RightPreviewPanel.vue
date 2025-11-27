<template>
  <div class="right-preview-panel">
    <!-- 面板头部工具栏 -->
    <div class="panel-header">
      <div class="header-left">
        <CheckCircle2 :size="18" class="header-icon" />
        <span class="header-title">信息图预览</span>
      </div>
      
      <div class="header-right" v-if="hasConfig">
        <!-- 模板选择器 -->
        <div class="template-selector" ref="dropdownRef">
          <button 
            class="selector-btn"
            @click="toggleDropdown"
          >
            <span class="selector-label">信息图类型:</span>
            <span class="selector-value">{{ currentTemplateName }}</span>
            <ChevronDown :size="14" :class="['selector-arrow', { 'rotated': isDropdownOpen }]" />
          </button>
          
          <!-- 下拉菜单 -->
          <div v-if="isDropdownOpen" class="dropdown-menu">
            <button
              v-for="rec in recommendations"
              :key="rec.templateId"
              class="dropdown-item"
              :class="{ 'active': selectedTemplateId === rec.templateId }"
              @click="handleTemplateSelect(rec.templateId)"
            >
              {{ rec.templateName }}
              <Check v-if="selectedTemplateId === rec.templateId" :size="14" />
            </button>
          </div>
        </div>
        
        <!-- 导出按钮（下拉菜单） -->
        <div class="export-dropdown" ref="exportDropdownRef">
          <button class="action-btn" @click="toggleExportDropdown">
            <Download :size="14" />
            <span class="btn-text">导出</span>
            <ChevronDown :size="12" :class="['dropdown-arrow', { 'rotated': isExportDropdownOpen }]" />
          </button>
          
          <!-- 导出格式下拉菜单 -->
          <div v-if="isExportDropdownOpen" class="export-dropdown-menu">
            <button class="export-item" @click="handleExport({ key: 'png' })">
              <span>🖼️ PNG 图片</span>
              <span class="export-desc">高清位图</span>
            </button>
            <button class="export-item" @click="handleExport({ key: 'svg' })">
              <span>🎨 SVG 矢量图</span>
              <span class="export-desc">可无限缩放</span>
            </button>
            <button class="export-item" @click="handleExport({ key: 'pptx' })">
              <span>📊 PPTX 演示</span>
              <span class="export-desc">PowerPoint</span>
            </button>
          </div>
        </div>
        
        <!-- 保存按钮 -->
        <button class="action-btn primary" @click="handleSave">
          <Save :size="14" />
          <span class="btn-text">保存</span>
        </button>
      </div>
    </div>

    <!-- 画布区域 -->
    <div class="panel-body">
      <!-- 空状态 -->
      <div v-if="!hasConfig" class="empty-state">
        <div class="empty-icon">
          <Maximize :size="32" />
        </div>
        <p class="empty-text">在左侧输入内容并点击分析<br/>即可生成预览</p>
      </div>
      
      <!-- 加载状态 -->
      <div v-else-if="isGenerating" class="loading-state">
        <div class="loading-spinner"></div>
        <p class="loading-text">正在生成信息图...</p>
      </div>
      
      <!-- 画布内容 -->
      <div v-else class="canvas-wrapper">
        <div 
          class="canvas-content"
          :style="{ transform: `scale(${zoomLevel})` }"
        >
          <div ref="canvasRef" class="canvas" id="infographic-canvas"></div>
        </div>
        
        <!-- 缩放控制 -->
        <div class="zoom-controls">
          <button class="zoom-btn" @click="handleZoomOut" title="缩小">
            <ZoomOut :size="16" />
          </button>
          <div class="zoom-divider"></div>
          <button class="zoom-btn fit" @click="handleZoomReset" title="适应">
            <Maximize :size="12" />
            <span>适应</span>
          </button>
          <div class="zoom-divider"></div>
          <button class="zoom-btn" @click="handleZoomIn" title="放大">
            <ZoomIn :size="16" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick, onUnmounted, onMounted } from 'vue'
import {
  Download,
  Save,
  ZoomIn,
  ZoomOut,
  Maximize,
  CheckCircle2,
  ChevronDown,
  Check
} from 'lucide-vue-next'
import { message } from 'ant-design-vue'
import { useWorkspaceStore } from '@/stores/workspace'
import { useTemplateStore } from '@/stores/template'
import { Infographic, registerResourceLoader, loadSVGResource } from '@antv/infographic'

// 注册资源加载器,用于加载图标
registerResourceLoader(async (config) => {
  const { data } = config
  
  try {
    // 处理 icon:xxx 格式的图标
    if (data.startsWith('icon:')) {
      const iconId = data.replace('icon:', '')
      // 使用 iconify API 加载图标
      const response = await fetch(`https://api.iconify.design/${iconId}.svg`)
      const svgText = await response.text()
      return loadSVGResource(svgText)
    }
    
    // 处理 illus:xxx 格式的插图
    if (data.startsWith('illus:')) {
      const illusId = data.replace('illus:', '')
      // 可以从其他来源加载插图
      // 这里暂时返回一个占位符
      return loadSVGResource('<svg xmlns="http://www.w3.org/2000/svg"></svg>')
    }
  } catch (error) {
    console.error('资源加载失败:', error)
  }
  
  return null
})

const workspaceStore = useWorkspaceStore()
const templateStore = useTemplateStore()

const canvasRef = ref<HTMLElement>()
const dropdownRef = ref<HTMLElement>()
const exportDropdownRef = ref<HTMLElement>()
const zoomLevel = ref(1)
const isDropdownOpen = ref(false)
const isExportDropdownOpen = ref(false)
let infographicInstance: any = null // 使用 any 避免类型问题

// 计算属性
const hasConfig = computed(() => workspaceStore.hasConfig)
const isGenerating = computed(() => workspaceStore.isGenerating)
const config = computed(() => workspaceStore.infographicConfig)
const recommendations = computed(() => templateStore.recommendations)

const selectedTemplateId = computed({
  get: () => workspaceStore.selectedTemplateId,
  set: (value) => {
    if (value) workspaceStore.setSelectedTemplate(value)
  }
})

const currentTemplateName = computed(() => {
  const current = recommendations.value.find(r => r.templateId === selectedTemplateId.value)
  return current?.templateName || '选择模板'
})

// 监听点击外部关闭下拉菜单
onMounted(() => {
  const handleClickOutside = (event: MouseEvent) => {
    if (dropdownRef.value && !dropdownRef.value.contains(event.target as Node)) {
      isDropdownOpen.value = false
    }
    if (exportDropdownRef.value && !exportDropdownRef.value.contains(event.target as Node)) {
      isExportDropdownOpen.value = false
    }
  }
  
  document.addEventListener('mousedown', handleClickOutside)
  
  // 组件卸载时移除监听
  onUnmounted(() => {
    document.removeEventListener('mousedown', handleClickOutside)
  })
})

// 监听配置变化，渲染信息图
watch(config, async (newConfig) => {  console.log('[RightPreviewPanel] config变化:', newConfig)
  // 确保配置有效且包含必要字段
  // 支持两种配置格式:
  // 1. template + data (如: list-row-horizontal-icon-arrow)
  // 2. design + data (如: checklist, pyramid-layer)
  const hasTemplate = !!(newConfig && (newConfig.template || newConfig.design))
  const hasData = !!(newConfig && newConfig.data)
  
  if (hasTemplate && hasData) {
    // 等待DOM更新，确保canvas元素已经渲染
    await nextTick()
    await nextTick() // 双重nextTick确保v-else条件渲染完成
    
    if (canvasRef.value) {
      console.log('[RightPreviewPanel] 准备渲染, config:', newConfig)
      renderInfographic(newConfig)
    } else {
      console.warn('[RightPreviewPanel] canvas容器未就绪')
    }
  } else {
    console.log('[RightPreviewPanel] 配置无效或不完整:', { hasTemplate: hasTemplate, hasData: hasData })
  }
}, { deep: true, immediate: true })

// 方法
function toggleDropdown() {
  isDropdownOpen.value = !isDropdownOpen.value
}

function toggleExportDropdown() {
  isExportDropdownOpen.value = !isExportDropdownOpen.value
}

async function handleTemplateSelect(templateId: string) {
  if (templateId === selectedTemplateId.value) {
    isDropdownOpen.value = false
    return
  }
  
  try {
    isDropdownOpen.value = false
    message.loading('正在切换模板...', 0)
    
    // 重新生成信息图
    workspaceStore.setGenerating(true)
    const generateModule = await import('@/api/generate')
    const response = await generateModule.generateAPI.extractData(workspaceStore.inputText, templateId)
    
    if (response.success && response.data) {
      workspaceStore.setSelectedTemplate(templateId)
      workspaceStore.setConfig(response.data.config)
      message.destroy()
      message.success('模板切换成功')
    }
  } catch (error: any) {
    message.destroy()
    message.error(error.message || '切换失败')
  } finally {
    workspaceStore.setGenerating(false)
  }
}

function renderInfographic(cfg: any) {
  try {
    console.log('渲染配置:', cfg)
    
    if (!canvasRef.value) {
      console.warn('画布容器不存在')
      return
    }
    
    // 销毁旧实例
    if (infographicInstance) {
      try {
        infographicInstance.destroy()
      } catch (e) {
        console.warn('销毁旧实例失败:', e)
      }
      infographicInstance = null
    }
    
    // 清空容器
    canvasRef.value.innerHTML = ''
    
    // 获取容器尺寸
    const containerWidth = canvasRef.value.offsetWidth || 800
    const containerHeight = canvasRef.value.parentElement?.offsetHeight || 600
    
    console.log('容器尺寸:', { width: containerWidth, height: containerHeight })
    
    // 创建新的Infographic实例
    infographicInstance = new Infographic({
      container: canvasRef.value,
      width: containerWidth,
      height: Math.max(containerHeight - 24, 500), // 减去padding，最小500px
      ...cfg
    })
    
    // 渲染
    infographicInstance.render()
    console.log('信息图渲染成功')
    message.success('信息图渲染成功')
  } catch (error: any) {
    console.error('渲染失败:', error)
    message.error(`渲染失败: ${error.message || '未知错误'}`)
  }
}

async function handleTemplateChange(templateId: string) {
  try {
    message.loading('正在切换模板...', 0)
    
    // 重新生成信息图
    workspaceStore.setGenerating(true)
    const generateModule = await import('@/api/generate')
    const response = await generateModule.generateAPI.extractData(workspaceStore.inputText, templateId)
    
    if (response.success && response.data) {
      workspaceStore.setConfig(response.data.config)
      message.destroy()
      message.success('模板切换成功')
    }
  } catch (error: any) {
    message.destroy()
    message.error(error.message || '切换失败')
  } finally {
    workspaceStore.setGenerating(false)
  }
}

function handleExportClick() {
  // 目前直接导出PNG
  handleExport({ key: 'png' })
}

async function handleExport({ key }: { key: string }) {
  try {
    // 关闭下拉菜单
    isExportDropdownOpen.value = false
    
    message.loading(`正在导出${key.toUpperCase()}...`, 0)
    
    // 检查是否有渲染实例
    if (!infographicInstance) {
      message.destroy()
      message.warning('请先生成信息图')
      return
    }
    
    // PNG 和 SVG 使用前端直接导出
    if (key === 'png' || key === 'svg') {
      try {
        const dataURL = await infographicInstance.toDataURL({
          type: key as 'png' | 'svg',
          dpr: 2  // 高清输出
        })
        
        // 下载文件
        const link = document.createElement('a')
        link.href = dataURL
        link.download = `infographic_${Date.now()}.${key}`
        link.click()
        
        message.destroy()
        message.success(`${key.toUpperCase()}导出成功`)
      } catch (error: any) {
        message.destroy()
        message.error(`导出失败: ${error.message || '未知错误'}`)
      }
      return
    }
    
    // PPTX 需要调用后端API
    if (key === 'pptx') {
      const svgElement = canvasRef.value?.querySelector('svg')
      if (!svgElement) {
        message.destroy()
        message.warning('请先生成信息图')
        return
      }
      
      console.log('开始导出PPTX...')
      const svgContent = new XMLSerializer().serializeToString(svgElement)
      console.log('SVG内容长度:', svgContent.length)
      
      try {
        // 调用导出API
        const { exportInfographic, getDownloadUrl } = await import('@/api/export')
        console.log('调用后端导出API...')
        
        const response = await exportInfographic({
          svgContent,
          format: 'pptx',
          filename: `infographic_${Date.now()}.pptx`,
          title: '信息图'
        })
        
        console.log('导出响应:', response)
        
        if (response.success && response.data) {
          message.destroy()
          
          // 下载文件
          const downloadUrl = getDownloadUrl(response.data.filename)
          console.log('下载URL:', downloadUrl)
          
          const link = document.createElement('a')
          link.href = downloadUrl
          link.download = response.data.filename
          link.click()
          
          message.success('PPTX导出成功')
        } else {
          message.destroy()
          message.error(response.error || '导出失败')
        }
      } catch (apiError: any) {
        console.error('导出API调用失败:', apiError)
        message.destroy()
        const errorMsg = apiError.response?.data?.error || apiError.message || '导出失败'
        message.error(`导出失败: ${errorMsg}`)
      }
      return
    }
    
    message.destroy()
    message.warning(`暂不支持 ${key.toUpperCase()} 格式`)
  } catch (error: any) {
    console.error('导出异常:', error)
    message.destroy()
    message.error(error.message || '导出失败')
  }
}

async function handleSave() {
  try {
    const workModule = await import('@/api/work')
    
    const response = await workModule.createWork({
      title: `信息图_${new Date().toLocaleString()}`,
      templateId: selectedTemplateId.value!,
      inputText: workspaceStore.inputText,
      infographicConfig: config.value!
    })
    
    if (response.success) {
      message.success('保存成功')
    }
  } catch (error: any) {
    message.error(error.message || '保存失败')
  }
}

function handleZoomIn() {
  zoomLevel.value = Math.min(zoomLevel.value + 0.1, 2)
  applyZoom()
}

function handleZoomOut() {
  zoomLevel.value = Math.max(zoomLevel.value - 0.1, 0.5)
  applyZoom()
}

function handleZoomReset() {
  zoomLevel.value = 1
  applyZoom()
}

function applyZoom() {
  if (canvasRef.value) {
    canvasRef.value.style.transform = `scale(${zoomLevel.value})`
  }
}

// 组件卸载时清理实例
onUnmounted(() => {
  if (infographicInstance) {
    try {
      infographicInstance.destroy()
    } catch (e) {
      console.warn('清理实例失败:', e)
    }
    infographicInstance = null
  }
})
</script>

<style scoped lang="scss">
.right-preview-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  border: 1px solid #f0f0f0;
  overflow: hidden;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #fff;
  border-bottom: 1px solid #f0f0f0;
  flex-shrink: 0;
  position: relative;
  z-index: 20;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-icon {
  color: #3b82f6;
}

.header-title {
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.template-selector {
  position: relative;
}

.selector-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  font-size: 13px;
  background: #f9fafb;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  
  &:hover {
    background: #f3f4f6;
    border-color: #3b82f6;
  }
  
  &:focus {
    outline: none;
    ring: 2px;
    ring-color: rgba(59, 130, 246, 0.1);
    border-color: #3b82f6;
  }
}

.selector-label {
  color: #6b7280;
}

.selector-value {
  color: #111827;
  font-weight: 500;
  min-width: 80px;
  text-align: left;
}

.selector-arrow {
  color: #6b7280;
  transition: transform 0.2s;
  
  &.rotated {
    transform: rotate(180deg);
  }
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 224px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  border: 1px solid #f0f0f0;
  overflow: hidden;
  z-index: 50;
  animation: fadeIn 0.1s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(-4px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.dropdown-item {
  width: 100%;
  text-align: left;
  padding: 10px 16px;
  font-size: 13px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.15s;
  color: #374151;
  
  &:hover {
    background: #f9fafb;
  }
  
  &.active {
    color: #3b82f6;
    background: #eff6ff;
    font-weight: 500;
  }
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  font-size: 13px;
  color: #374151;
  background: #fff;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  
  &:hover {
    background: #f9fafb;
    color: #3b82f6;
  }
  
  &.primary {
    color: white;
    background: #3b82f6;
    border-color: #3b82f6;
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    
    &:hover {
      background: #2563eb;
      border-color: #2563eb;
    }
  }
}

.export-dropdown {
  position: relative;
}

.dropdown-arrow {
  color: #6b7280;
  transition: transform 0.2s;
  
  &.rotated {
    transform: rotate(180deg);
  }
}

.export-dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 200px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  border: 1px solid #f0f0f0;
  overflow: hidden;
  z-index: 50;
  animation: fadeIn 0.1s ease-out;
}

.export-item {
  width: 100%;
  text-align: left;
  padding: 12px 16px;
  font-size: 13px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.15s;
  color: #374151;
  
  &:hover {
    background: #f9fafb;
  }
  
  span:first-child {
    font-weight: 500;
  }
  
  .export-desc {
    font-size: 11px;
    color: #9ca3af;
    font-weight: 400;
  }
}

.btn-text {
  @media (max-width: 640px) {
    display: none;
  }
}

.panel-body {
  flex: 1;
  position: relative;
  min-height: 0;
  overflow: hidden;
  background: #f9fafb;
}

.empty-state,
.loading-state {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.empty-icon {
  width: 96px;
  height: 96px;
  background: #f3f4f6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #d1d5db;
}

.empty-text {
  text-align: center;
  color: #9ca3af;
  font-size: 14px;
  line-height: 1.6;
  margin: 0;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e5e7eb;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-text {
  color: #6b7280;
  font-size: 14px;
  margin: 0;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.canvas-wrapper {
  height: 100%;
  padding: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.canvas-content {
  transition: transform 0.3s ease-out;
  transform-origin: center;
  background: #fff;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  padding: 32px 48px;
  max-width: 100%;
  max-height: 100%;
}

.canvas {
  width: 100%;
  min-height: 400px;
}

.zoom-controls {
  position: absolute;
  bottom: 24px;
  right: 24px;
  background: #fff;
  border-radius: 9999px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid #f0f0f0;
  padding: 4px;
  display: flex;
  align-items: center;
  gap: 4px;
  z-index: 10;
}

.zoom-btn {
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  border-radius: 50%;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
  
  &:hover {
    background: #f3f4f6;
  }
  
  &.fit {
    padding: 4px 8px;
    gap: 4px;
    border-radius: 9999px;
    font-size: 12px;
    font-weight: 500;
    color: #4b5563;
  }
}

.zoom-divider {
  width: 1px;
  height: 16px;
  background: #e5e7eb;
}
</style>
