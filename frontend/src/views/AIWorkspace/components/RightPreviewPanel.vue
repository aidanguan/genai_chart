<template>
  <div class="right-preview-panel">
    <!-- 面板头部工具栏 -->
    <div class="panel-header">
      <div class="header-left">
        <CheckCircle2 :size="18" class="header-icon" />
        <span class="header-title">信息图预览</span>
      </div>
      
      <div class="header-right" v-if="hasConfig">
        <!-- 配色调整按钮 -->
        <button class="action-btn" @click="togglePropertyPanel" :class="{ 'active': propertyPanelVisible }">
          <Settings :size="14" />
          <span class="btn-text">配色</span>
        </button>
        
        <!-- 查看代码按钮 -->
        <button class="action-btn" @click="showConfigViewer">
          <Code :size="14" />
          <span class="btn-text">查看代码</span>
        </button>
        
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
        
        <!-- 分享到示例按钮 -->
        <button class="action-btn" @click="showShareDialog">
          <Share2 :size="14" />
          <span class="btn-text">分享到示例</span>
        </button>
      </div>
    </div>

    <!-- 画布区域 -->
    <div class="panel-body">
      <!-- 主要内容区域 -->
      <div class="body-content">
        <!-- 左侧模板列表边栏 -->
        <TemplateListBar />
        
        <!-- 右侧画布区域 -->
        <div class="canvas-area">
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
        
        <!-- 属性编辑器 -->
        <PropertyPanel 
          v-model:visible="propertyPanelVisible"
          :selectedElement="selectedElement"
          :config="config"
          @text-change="handleTextChange"
          @visibility-change="handleVisibilityChange"
          @color-change="handleColorChange"
        />
      </div>
    </div>
    
    <!-- 配置JSON查看器弹窗 -->
    <ConfigJsonViewer 
      v-model:visible="configViewerVisible" 
      :config="config" 
    />
    
    <!-- 分享到示例对话框 -->
    <ShareToExamplesDialog 
      v-model:visible="shareDialogVisible" 
      :config="config"
      :inputText="workspaceStore.inputText"
      @success="handleShareSuccess"
    />
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
  Check,
  Code,
  Share2,
  Settings
} from 'lucide-vue-next'
import { message } from 'ant-design-vue'
import { useWorkspaceStore } from '@/stores/workspace'
import { useTemplateStore } from '@/stores/template'
import { Infographic, registerResourceLoader, loadSVGResource } from '@antv/infographic'
import TemplateListBar from './TemplateListBar.vue'
import ConfigJsonViewer from './ConfigJsonViewer.vue'
import ShareToExamplesDialog from './ShareToExamplesDialog.vue'
import PropertyPanel from './PropertyPanel.vue'

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
const exportDropdownRef = ref<HTMLElement>()
const zoomLevel = ref(1)
const isExportDropdownOpen = ref(false)
const configViewerVisible = ref(false) // 配置JSON查看器显示状态
const shareDialogVisible = ref(false) // 分享对话框显示状态
const propertyPanelVisible = ref(false) // 属性面板显示状态
const selectedElement = ref<any>(null) // 当前选中的元素
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
  // 兼容templateName可能不存在的情况
  return current?.templateName || current?.reason || '选择模板'
})

// 监听点击外部关闭下拉菜单
onMounted(() => {
  const handleClickOutside = (event: MouseEvent) => {
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
function togglePropertyPanel() {
  propertyPanelVisible.value = !propertyPanelVisible.value
}

function toggleExportDropdown() {
  isExportDropdownOpen.value = !isExportDropdownOpen.value
}

// 显示配置JSON查看器
function showConfigViewer() {
  configViewerVisible.value = true
}

// 显示分享对话框
function showShareDialog() {
  shareDialogVisible.value = true
}

// 分享成功回调
function handleShareSuccess() {
  // 可选：分享成功后的处理
  message.success('作品已成功分享到示例库')
}

// 属性面板相关处理函数
function handleTextChange(data: { path: string; value: string }) {
  // 更新配置中的文本内容
  console.log('文本变更:', data)
  
  const currentConfig = workspaceStore.infographicConfig
  if (!currentConfig) return
  
  // 创建新的配置对象
  const newConfig = JSON.parse(JSON.stringify(currentConfig))
  
  // 根据path更新对应的值
  // path格式: "data.title" 或 "data.items[0].label"
  const pathParts = data.path.split('.')
  let target: any = newConfig
  
  // 遍历路径，找到目标对象
  for (let i = 0; i < pathParts.length - 1; i++) {
    const part = pathParts[i]
    // 处理数组索引，如 items[0]
    const arrayMatch = part.match(/(\w+)\[(\d+)\]/)
    if (arrayMatch) {
      const [, key, index] = arrayMatch
      target = target[key][parseInt(index)]
    } else {
      target = target[part]
    }
  }
  
  // 设置最细的值
  const lastPart = pathParts[pathParts.length - 1]
  const arrayMatch = lastPart.match(/(\w+)\[(\d+)\]/)
  if (arrayMatch) {
    const [, key, index] = arrayMatch
    target[key][parseInt(index)] = data.value
  } else {
    target[lastPart] = data.value
  }
  
  // 更新store中的配置，触发重新渲染
  workspaceStore.setConfig(newConfig)
  message.success('文本已更新')
}

function handleVisibilityChange(data: { path: string; visible: boolean }) {
  // 更新元素可见性
  console.log('可见性变更:', data)
  
  const currentConfig = workspaceStore.infographicConfig
  if (!currentConfig) return
  
  // 创建新的配置对象
  const newConfig = JSON.parse(JSON.stringify(currentConfig))
  
  // 根据path查找目标元素
  const pathParts = data.path.split('.')
  let target: any = newConfig
  let parent: any = null
  let lastKey: string = ''
  
  // 遍历路径，找到目标对象的父级
  for (let i = 0; i < pathParts.length - 1; i++) {
    const part = pathParts[i]
    parent = target
    const arrayMatch = part.match(/(\w+)\[(\d+)\]/)
    if (arrayMatch) {
      const [, key, index] = arrayMatch
      target = target[key][parseInt(index)]
      lastKey = key
    } else {
      target = target[part]
      lastKey = part
    }
  }
  
  const finalKey = pathParts[pathParts.length - 1]
  
  if (data.visible) {
    // 显示元素 - 仅需记录日志，不需修改配置
    message.success('元素已显示')
  } else {
    // 隐藏元素 - 将字段值置为空或删除
    const arrayMatch = finalKey.match(/(\w+)\[(\d+)\]/)
    if (arrayMatch) {
      const [, key, index] = arrayMatch
      // 删除数组中的该项
      target[key].splice(parseInt(index), 1)
    } else {
      // 将字段置为空字符串
      target[finalKey] = ''
    }
    message.success('元素已隐藏')
  }
  
  // 更新store中的配置，触发重新渲染
  workspaceStore.setConfig(newConfig)
}

function handleColorChange(data: { type: 'primary' | 'bg' | 'palette'; value: any }) {
  // 更新配色方案
  console.log('配色变更:', data)
  
  const currentConfig = workspaceStore.infographicConfig
  if (!currentConfig) return
  
  // 创建新的配置对象
  const newConfig = JSON.parse(JSON.stringify(currentConfig))
  
  // 确保themeConfig存在
  if (!newConfig.themeConfig) {
    newConfig.themeConfig = {}
  }
  
  // 根据类型更新配置
  if (data.type === 'primary') {
    newConfig.themeConfig.colorPrimary = data.value
    // 清空调色板，让主色生效（因为palette优先级更高）
    delete newConfig.themeConfig.palette
    message.success('主色调已更新')
  } else if (data.type === 'bg') {
    newConfig.themeConfig.colorBg = data.value
    message.success('背景色已更新')
  } else if (data.type === 'palette') {
    if (data.value === null || data.value === undefined) {
      // 清空调色板，使用主色
      delete newConfig.themeConfig.palette
      message.success('已切换为使用主色')
    } else {
      newConfig.themeConfig.palette = data.value
      message.success('调色板已更新')
    }
  }
  
  // 更新store中的配置，触发重新渲染
  workspaceStore.setConfig(newConfig)
}

async function handleTemplateSelect(templateId: string) {
  if (templateId === selectedTemplateId.value) {
    return
  }
  
  try {
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
    console.log('========== 渲染配置详情 ==========')
    console.log('1. 原始配置:', JSON.stringify(cfg, null, 2))
    console.log('2. template:', cfg.template)
    console.log('3. design:', cfg.design)
    console.log('4. data.items:', cfg.data?.items)
    
    if (cfg.data?.items) {
      cfg.data.items.forEach((item: any, index: number) => {
        console.log(`   根节点${index + 1}: label="${item.label}", children=${item.children?.length}`)
        if (item.children) {
          item.children.forEach((child: any, ci: number) => {
            console.log(`     Child${ci + 1}: ${child.label} - ${child.desc}`)
          })
        }
      })
    }
    console.log('==================================')
    
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
    
    // 渲染完成后，为SVG元素添加点击事件监听器
    nextTick(() => {
      attachElementListeners()
    })
  } catch (error: any) {
    console.error('渲染失败:', error)
    message.error(`渲染失败: ${error.message || '未知错误'}`)
  }
}

// 为SVG元素添加点击监听器，实现元素选中机制和直接编辑
function attachElementListeners() {
  if (!canvasRef.value) return
  
  const svgElement = canvasRef.value.querySelector('svg')
  if (!svgElement) return
  
  // 查找所有可编辑的文本元素(包括 text 和 foreignObject 中的文本)
  const textElements = svgElement.querySelectorAll('text, foreignObject')
  
  textElements.forEach((element) => {
    // 添加样式，使元素可点击
    const targetEl = element as SVGElement
    targetEl.style.cursor = 'text'
    targetEl.classList.add('editable-text')
    
    // 如果是foreignObject，为内部的span添加contenteditable
    if (element.tagName === 'foreignObject') {
      const span = element.querySelector('span')
      if (span) {
        span.setAttribute('contenteditable', 'true')
        span.style.outline = 'none'
        span.style.cursor = 'text'
        
        // 保存原始文本，用于检测变更
        let originalText = span.textContent || ''
        
        // 点击时选中所有文本
        span.addEventListener('click', (e) => {
          e.stopPropagation()
          // 选中当前元素
          handleElementClick(element as SVGElement)
          // 自动选中文本内容
          const selection = window.getSelection()
          const range = document.createRange()
          range.selectNodeContents(span)
          selection?.removeAllRanges()
          selection?.addRange(range)
        })
        
        // 聚焦时保存原始文本
        span.addEventListener('focus', () => {
          originalText = span.textContent || ''
          targetEl.classList.add('editing')
          targetEl.style.outline = '2px solid #3b82f6'
          targetEl.style.outlineOffset = '2px'
        })
        
        // 失焦时保存修改
        span.addEventListener('blur', () => {
          targetEl.classList.remove('editing')
          const newText = span.textContent || ''
          
          if (newText !== originalText && newText.trim() !== '') {
            // 文本已修改，保存到配置
            saveTextEdit(element as SVGElement, originalText, newText)
          } else if (newText.trim() === '') {
            // 文本被清空，恢复原文本
            span.textContent = originalText
            message.warning('文本不能为空')
          }
          
          // 清除选中状态
          if (!targetEl.classList.contains('selected')) {
            targetEl.style.outline = ''
            targetEl.style.outlineOffset = ''
          }
        })
        
        // 按Enter键时失焦保存
        span.addEventListener('keydown', (e) => {
          if (e.key === 'Enter') {
            e.preventDefault()
            span.blur()
          }
          // Esc键取消编辑
          if (e.key === 'Escape') {
            e.preventDefault()
            span.textContent = originalText
            span.blur()
          }
        })
      }
    } else {
      // 对于普通text元素，保留原有的双击编辑面板功能
      element.addEventListener('dblclick', (e) => {
        e.stopPropagation()
        handleElementClick(element as SVGElement)
        propertyPanelVisible.value = true
      })
    }
    
    // 添加悬停效果
    element.addEventListener('mouseenter', () => {
      if (!targetEl.classList.contains('editing')) {
        targetEl.style.outline = '2px solid rgba(59, 130, 246, 0.3)'
        targetEl.style.outlineOffset = '2px'
      }
    })
    
    element.addEventListener('mouseleave', () => {
      if (!targetEl.classList.contains('selected') && !targetEl.classList.contains('editing')) {
        targetEl.style.outline = ''
        targetEl.style.outlineOffset = ''
      }
    })
    
    // 单击选中
    element.addEventListener('click', (e) => {
      // foreignObject的点击由内部span处理
      if (element.tagName !== 'foreignObject') {
        e.stopPropagation()
        handleElementClick(element as SVGElement)
      }
    })
  })
  
  // 点击画布空白处取消选中
  svgElement.addEventListener('click', () => {
    clearSelection()
  })
  
  console.log(`已为 ${textElements.length} 个文本元素添加交互监听器（支持直接编辑）`)
}

// 处理元素点击
function handleElementClick(element: SVGElement) {
  // 获取文本内容
  let textContent = ''
  if (element.tagName === 'foreignObject') {
    const span = element.querySelector('span')
    textContent = span?.textContent || ''
  } else {
    textContent = element.textContent || ''
  }
  
  // 尝试从元素的data属性中获取路径信息
  const elementId = element.getAttribute('id') || ''
  const dataType = element.getAttribute('data-element-type') || ''
  
  // 智能推断元素类型和路径
  let elementType: 'title' | 'desc' | 'item' | 'item-field' = 'item-field'
  let path = ''
  
  // 根据ID和内容推断路径
  if (elementId.includes('title') || dataType === 'title') {
    elementType = 'title'
    path = 'data.title'
  } else if (elementId.includes('desc') || dataType === 'desc' || dataType === 'description') {
    elementType = 'desc'
    path = 'data.desc'
  } else {
    // 尝试从配置中查找匹配的文本
    const currentConfig = workspaceStore.infographicConfig
    if (currentConfig?.data) {
      const found = findTextInConfig(currentConfig.data, textContent)
      if (found) {
        path = found.path
        elementType = found.type as any
      } else {
        // 默认处理：假设是items中的某个字段
        path = 'data.items[0].label'
        elementType = 'item-field'
      }
    }
  }
  
  // 清除之前的选中状态
  clearSelection()
  
  // 设置选中元素
  selectedElement.value = {
    type: elementType,
    path: path,
    value: textContent
  }
  
  // 添加选中样式
  element.classList.add('selected')
  element.style.outline = '2px solid #3b82f6'
  element.style.outlineOffset = '2px'
  
  // 【FORCE UPDATE】最后更新: 2025-11-30 - 移除了弹窗提示
  console.log('[UPDATED 2025-11-30] 选中元素 (无弹窗):', selectedElement.value)
}

// 在配置中查找文本的路径
function findTextInConfig(data: any, text: string, prefix = 'data'): { path: string; type: string } | null {
  // 检查标题
  if (data.title === text) {
    return { path: `${prefix}.title`, type: 'title' }
  }
  
  // 检查描述
  if (data.desc === text || data.description === text) {
    return { path: `${prefix}.desc`, type: 'desc' }
  }
  
  // 检查items数组
  if (Array.isArray(data.items)) {
    for (let i = 0; i < data.items.length; i++) {
      const item = data.items[i]
      
      // 检查item的各个字段
      if (item.label === text) {
        return { path: `${prefix}.items[${i}].label`, type: 'item-field' }
      }
      if (item.value === text) {
        return { path: `${prefix}.items[${i}].value`, type: 'item-field' }
      }
      if (item.desc === text || item.description === text) {
        return { path: `${prefix}.items[${i}].desc`, type: 'item-field' }
      }
      if (item.title === text) {
        return { path: `${prefix}.items[${i}].title`, type: 'item-field' }
      }
    }
  }
  
  return null
}

// 清除选中状态
function clearSelection() {
  if (!canvasRef.value) return
  
  const svgElement = canvasRef.value.querySelector('svg')
  if (!svgElement) return
  
  // 清除所有选中状态
  const selectedElements = svgElement.querySelectorAll('.selected')
  selectedElements.forEach((el) => {
    el.classList.remove('selected')
    ;(el as SVGElement).style.outline = ''
    ;(el as SVGElement).style.outlineOffset = ''
  })
}

// 保存文本编辑
function saveTextEdit(element: SVGElement, oldText: string, newText: string) {
  console.log('保存文本编辑:', { oldText, newText })
  
  const currentConfig = workspaceStore.infographicConfig
  if (!currentConfig?.data) return
  
  // 尝试从配置中查找旧文本的路径
  const found = findTextInConfig(currentConfig.data, oldText)
  
  if (found) {
    // 找到了路径，更新配置
    const newConfig = JSON.parse(JSON.stringify(currentConfig))
    const pathParts = found.path.split('.')
    let target: any = newConfig
    
    // 遍历路径，找到目标对象
    for (let i = 0; i < pathParts.length - 1; i++) {
      const part = pathParts[i]
      // 处理数组索引，如 items[0]
      const arrayMatch = part.match(/(\w+)\[(\d+)\]/)
      if (arrayMatch) {
        const [, key, index] = arrayMatch
        target = target[key][parseInt(index)]
      } else {
        target = target[part]
      }
    }
    
    // 设置新值
    const lastPart = pathParts[pathParts.length - 1]
    const arrayMatch = lastPart.match(/(\w+)\[(\d+)\]/)
    if (arrayMatch) {
      const [, key, index] = arrayMatch
      target[key][parseInt(index)] = newText
    } else {
      target[lastPart] = newText
    }
    
    // 更新store中的配置，触发重新渲染
    workspaceStore.setConfig(newConfig)
    message.success('文本已更新')
  } else {
    // 未找到路径，提示用户
    message.warning('无法定位文本在配置中的位置，请使用属性面板编辑')
    console.warn('未找到文本路径:', oldText)
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
  padding: 4px 8px;
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
  
  &.active {
    color: #3b82f6;
    border-color: #3b82f6;
    background: #eff6ff;
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

.toolbar-dropdown {
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

.toolbar-dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 220px;
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

.toolbar-item {
  width: 100%;
  text-align: left;
  padding: 12px 16px;
  font-size: 13px;
  display: flex;
  flex-direction: column;
  gap: 4px;
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
  
  .toolbar-desc {
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
  display: flex;
}

.body-content {
  flex: 1;
  display: flex;
  gap: 0;
  min-height: 0;
  margin: 0;
}

.canvas-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}

.empty-state,
.loading-state {
  flex: 1;
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
  flex: 1;
  padding: 0;
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
  border-radius: 6px;
  padding: 4px 6px;
  max-width: 100%;
  max-height: 100%;
}

.canvas {
  width: 100%;
  min-height: 400px;
  
  // 为可编辑文本添加全局样式
  :deep(.editable-text) {
    transition: all 0.2s ease;
    
    &:hover {
      outline: 2px solid rgba(59, 130, 246, 0.3) !important;
      outline-offset: 2px !important;
    }
    
    &.selected {
      outline: 2px solid #3b82f6 !important;
      outline-offset: 2px !important;
    }
    
    &.editing {
      outline: 2px solid #3b82f6 !important;
      outline-offset: 2px !important;
      background: rgba(59, 130, 246, 0.05);
    }
  }
  
  // 为 contenteditable 的 span 添加样式
  :deep(foreignObject span[contenteditable="true"]) {
    outline: none;
    cursor: text;
    user-select: text;
    -webkit-user-select: text;
    -moz-user-select: text;
    -ms-user-select: text;
    
    &:focus {
      outline: none;
      background: rgba(59, 130, 246, 0.05);
    }
  }
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

// 工具栏折叠按钮样式
.toolbar-toggle-collapsed {
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
  
  .toggle-btn {
    padding: 6px 12px;
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    color: #6b7280;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 4px;
    
    &:hover {
      background: #f3f4f6;
      border-color: #d1d5db;
    }
  }
}
</style>
