<template>
  <div class="right-preview-panel">
    <div class="panel-header">
      <div class="header-left">
        <h2 class="panel-title">信息图预览</h2>
      </div>
      
      <div class="header-right" v-if="hasConfig">
        <a-space>
          <!-- 模板选择器 -->
          <a-select
            v-model:value="selectedTemplateId"
            style="width: 200px"
            placeholder="选择模板"
            @change="handleTemplateChange"
          >
            <a-select-option
              v-for="rec in recommendations"
              :key="rec.templateId"
              :value="rec.templateId"
            >
              {{ rec.templateName }} ({{ rec.matchScore }}%)
            </a-select-option>
          </a-select>
          
          <!-- 导出按钮 -->
          <a-dropdown>
            <template #overlay>
              <a-menu @click="handleExport">
                <a-menu-item key="svg">
                  <FileImageOutlined /> 导出SVG
                </a-menu-item>
                <a-menu-item key="png">
                  <PictureOutlined /> 导出PNG
                </a-menu-item>
                <a-menu-item key="pdf" disabled>
                  <FilePdfOutlined /> 导出PDF (开发中)
                </a-menu-item>
                <a-menu-item key="pptx" disabled>
                  <FileWordOutlined /> 导出PPTX (开发中)
                </a-menu-item>
              </a-menu>
            </template>
            <a-button>
              <DownloadOutlined /> 导出
            </a-button>
          </a-dropdown>
          
          <!-- 保存按钮 -->
          <a-button type="primary" @click="handleSave">
            <SaveOutlined /> 保存
          </a-button>
        </a-space>
      </div>
    </div>
    
    <div class="panel-body">
      <!-- 空状态 -->
      <div v-if="!hasConfig" class="empty-state">
         <a-empty description="请在左侧输入内容并点击「分析并推荐模板」开始">
          <template #image>
            <FileSearchOutlined style="font-size: 64px; color: #d9d9d9;" />
          </template>
        </a-empty>
      </div>
      
      <!-- 加载状态 -->
      <div v-else-if="isGenerating" class="loading-state">
        <a-spin size="large" tip="正在生成信息图...">
          <div class="spin-content"></div>
        </a-spin>
      </div>
      
      <!-- 画布区域 -->
      <div v-else class="canvas-container">
        <div ref="canvasRef" class="canvas" id="infographic-canvas"></div>
      </div>
    </div>
    
    <!-- 底部操作栏 -->
    <div class="panel-footer" v-if="hasConfig">
      <a-space>
        <a-button-group>
          <a-button @click="handleZoomOut">
            <ZoomOutOutlined /> 缩小
          </a-button>
          <a-button @click="handleZoomReset">
            <FullscreenOutlined /> 适应
          </a-button>
          <a-button @click="handleZoomIn">
            <ZoomInOutlined /> 放大
          </a-button>
        </a-button-group>
      </a-space>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick, onUnmounted } from 'vue'
import {
  DownloadOutlined,
  SaveOutlined,
  FileImageOutlined,
  PictureOutlined,
  FilePdfOutlined,
  FileWordOutlined,
  FileSearchOutlined,
  ZoomInOutlined,
  ZoomOutOutlined,
  FullscreenOutlined
} from '@ant-design/icons-vue'
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
const zoomLevel = ref(1)
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
  } catch (error) {
    console.error('渲染失败:', error)
    message.error('渲染失败')
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

async function handleExport({ key }: { key: string }) {
  try {
    message.loading(`正在导出${key.toUpperCase()}...`, 0)
    
    // 获取SVG内容
    const svgElement = canvasRef.value?.querySelector('svg')
    if (!svgElement) {
      message.destroy()
      message.warning('请先生成信息图')
      return
    }
    
    const svgContent = new XMLSerializer().serializeToString(svgElement)
    
    // 调用导出API
    const { exportInfographic, getDownloadUrl } = await import('@/api/export')
    const response = await exportInfographic({
      svgContent,
      format: key as 'svg' | 'png' | 'pdf' | 'pptx',
      filename: `infographic_${Date.now()}.${key}`,
      title: '信息图',
      width: 1200,
      height: 800,
      scale: 2
    })
    
    if (response.success && response.data) {
      message.destroy()
      
      // 下载文件
      const downloadUrl = getDownloadUrl(response.data.filename)
      const link = document.createElement('a')
      link.href = downloadUrl
      link.download = response.data.filename
      link.click()
      
      message.success(`${key.toUpperCase()}导出成功`)
    }
  } catch (error: any) {
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
}

.panel-title {
  margin: 0;
  font-size: 16px;
  font-weight: 500;
  color: #262626;
}

.panel-body {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  position: relative;
  min-height: 0;
}

.empty-state,
.loading-state {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.spin-content {
  height: 200px;
}

.canvas-container {
  padding: 12px;
  min-height: 100%;
  display: flex;
  align-items: flex-start;
  justify-content: center;
}

.canvas {
  width: 100%;
  min-height: 500px;
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  transform-origin: top center;
  width: 100%;
  max-width: 1200px;
}

.panel-footer {
  padding: 12px 16px;
  background: #fff;
  border-top: 1px solid #f0f0f0;
  display: flex;
  justify-content: center;
  flex-shrink: 0;
}
</style>
