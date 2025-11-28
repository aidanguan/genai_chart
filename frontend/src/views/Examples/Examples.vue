<template>
  <div class="examples-page">
    <!-- Header -->
    <WorkspaceHeader />
    
    <!-- Main Content -->
    <main class="examples-main">
      <div class="examples-container">
        <!-- 页面标题 -->
        <div class="page-header">
          <h1 class="page-title">模板示例</h1>
          <p class="page-subtitle">浏览所有可用的信息图模板，共 {{ totalCount }} 个模板</p>
        </div>
        
        <!-- 分类筛选 -->
        <div class="category-filter">
          <button 
            class="filter-button"
            :class="{ 'active': selectedCategory === null }"
            @click="selectCategory(null)"
          >
            全部 ({{ totalCount }})
          </button>
          <button 
            v-for="cat in categories"
            :key="cat.code"
            class="filter-button"
            :class="{ 'active': selectedCategory === cat.code }"
            @click="selectCategory(cat.code)"
          >
            {{ cat.icon }} {{ cat.name }} ({{ cat.count }})
          </button>
        </div>
        
        <!-- 加载状态 -->
        <div v-if="loading" class="loading-container">
          <div class="loading-spinner"></div>
          <p class="loading-text">加载中...</p>
        </div>
        
        <!-- 模板网格 -->
        <div v-else class="templates-grid">
          <div 
            v-for="(template, index) in filteredTemplates"
            :key="template.id"
            class="template-card"
            @click="handleTemplateClick(template)"
          >
            <!-- 预览区域 -->
            <div class="card-preview">
              <div :ref="el => setPreviewRef(el, index)" class="preview-canvas"></div>
            </div>
            
            <div class="card-header">
              <h3 class="card-title">{{ template.name }}</h3>
              <span class="card-badge">{{ getCategoryName(template.category) }}</span>
            </div>
            <p class="card-description">{{ template.description }}</p>
            <div class="card-footer">
              <div class="card-tags">
                <span 
                  v-for="tag in getTemplateTags(template)"
                  :key="tag"
                  class="tag"
                >
                  {{ tag }}
                </span>
              </div>
            </div>
            <div class="card-overlay">
              <div class="overlay-content">
                <button class="preview-button">查看详情</button>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 空状态 -->
        <div v-if="!loading && filteredTemplates.length === 0" class="empty-state">
          <p class="empty-text">暂无模板</p>
        </div>
      </div>
    </main>
    
    <!-- 模板预览弹窗 -->
    <div v-if="selectedTemplate" class="modal-overlay" @click.self="closePreview">
      <div class="modal-content">
        <div class="modal-header">
          <h2 class="modal-title">{{ selectedTemplate.name }}</h2>
          <button class="close-button" @click="closePreview">
            <X :size="24" />
          </button>
        </div>
        <div class="modal-body">
          <div class="template-info">
            <div class="info-row">
              <span class="info-label">分类：</span>
              <span class="info-value">{{ getCategoryName(selectedTemplate.category) }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">描述：</span>
              <span class="info-value">{{ selectedTemplate.description }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">适用场景：</span>
              <span class="info-value">{{ selectedTemplate.use_cases || '多种场景' }}</span>
            </div>
            <div class="info-row" v-if="selectedTemplate.tags && selectedTemplate.tags.length > 0">
              <span class="info-label">标签：</span>
              <div class="info-tags">
                <span 
                  v-for="tag in selectedTemplate.tags"
                  :key="tag"
                  class="info-tag"
                >
                  {{ tag }}
                </span>
              </div>
            </div>
          </div>
          <div class="template-preview">
            <div ref="detailPreviewRef" class="detail-preview-canvas"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { X } from 'lucide-vue-next'
import WorkspaceHeader from '@/views/AIWorkspace/components/WorkspaceHeader.vue'
import { getTemplates, getCategories } from '@/api/templates'
import { Infographic, registerResourceLoader, loadSVGResource } from '@antv/infographic'

// 注册资源加载器,用于加载图标
registerResourceLoader(async (config) => {
  const { data } = config
  
  try {
    if (data.startsWith('icon:')) {
      const iconId = data.replace('icon:', '')
      const response = await fetch(`https://api.iconify.design/${iconId}.svg`)
      const svgText = await response.text()
      return loadSVGResource(svgText)
    }
  } catch (error) {
    console.error('资源加载失败:', error)
  }
  
  return null
})

interface Template {
  id: string
  name: string
  category: string
  description: string
  use_cases?: string
  tags?: string[]
  dataSchema?: any
  designConfig?: any
}

interface Category {
  code: string
  name: string
  description: string
  count: number
  icon: string
}

// 状态
const loading = ref(false)
const templates = ref<Template[]>([])
const categories = ref<Category[]>([])
const selectedCategory = ref<string | null>(null)
const selectedTemplate = ref<Template | null>(null)
const previewRefs = ref<(HTMLElement | null)[]>([])
const detailPreviewRef = ref<HTMLElement | null>(null)

// 计算属性
const totalCount = computed(() => templates.value.length)

const filteredTemplates = computed(() => {
  if (!selectedCategory.value) return templates.value
  return templates.value.filter(t => t.category === selectedCategory.value)
})

// 分类映射
const categoryMap: Record<string, { name: string; icon: string }> = {
  'sequence': { name: '顺序型', icon: '🔄' },
  'list': { name: '列表型', icon: '📋' },
  'comparison': { name: '对比型', icon: '⚖️' },
  'relation': { name: '关系型', icon: '🔗' },
  'hierarchy': { name: '层级型', icon: '🏔️' },
  'chart': { name: '图表型', icon: '📊' },
  'quadrant': { name: '四象限型', icon: '🎯' }
}

// 方法
const setPreviewRef = (el: any, index: number) => {
  if (el) {
    previewRefs.value[index] = el as HTMLElement
  }
}

const getCategoryName = (code: string) => {
  return categoryMap[code]?.name || code
}

const getTemplateTags = (template: Template) => {
  if (template.tags && template.tags.length > 0) {
    return template.tags.slice(0, 3)
  }
  return []
}

const selectCategory = (category: string | null) => {
  selectedCategory.value = category
  // 清空 refs 以便重新收集
  previewRefs.value = []
  // 等待DOM更新后重新渲染预览
  nextTick(() => {
    setTimeout(() => renderPreviews(), 100)
  })
}

const handleTemplateClick = (template: Template) => {
  selectedTemplate.value = template
  // 等待弹窗 DOM 渲染后再渲染信息图
  nextTick(() => {
    setTimeout(() => renderDetailPreview(template), 50)
  })
}

const closePreview = () => {
  selectedTemplate.value = null
  // 清空详情预览容器
  if (detailPreviewRef.value) {
    detailPreviewRef.value.innerHTML = ''
  }
}

// 渲染详情弹窗中的信息图
const renderDetailPreview = (template: Template) => {
  const container = detailPreviewRef.value
  if (!container) {
    console.warn('详情预览容器未找到')
    return
  }
  
  try {
    // 清空容器
    container.innerHTML = ''
    
    const sampleData = generateSampleData(template)
    // 获取该模板的主题色（使用 0 作为索引，确保一致性）
    const themeColors = getThemeColors(template, 0)
    
    // 构建配置对象（复用 renderPreviews 中的逻辑）
    let config: any = {}
    
    // 内置模板映射
    const builtInTemplateMap: Record<string, string> = {
      'compare-binary-horizontal': 'compare-binary-horizontal-badge-card-arrow',
      'compare-binary-vs-card': 'compare-binary-horizontal-badge-card-vs',
      'compare-hierarchy-left-right': 'compare-hierarchy-left-right-circle-node-pill-badge',
      'compare-hierarchy-row': 'compare-swot',
      'comparison-two-column': 'compare-binary-horizontal-compact-card-fold',
      'relation-circle': 'relation-circle-icon-badge',
      'relation-circle-connected': 'relation-circle-icon-badge',
      'relation-network': 'relation-circle-icon-badge',
      'mindmap-radial': 'relation-circle-icon-badge',
      'list-column-simple': 'list-column-simple-vertical-arrow',
      'list-grid': 'list-grid-simple',
      'list-grid-icon-card': 'list-grid-badge-card',
      'list-grid-badge-card': 'list-grid-badge-card',
      'list-row': 'list-row-simple-horizontal-arrow',
      'list-row-icon-badge': 'list-row-horizontal-icon-arrow',
      'checklist': 'list-column-done-list'
    }
    
    if (builtInTemplateMap[template.id]) {
      config = { template: builtInTemplateMap[template.id] }
    } else if (template.designConfig) {
      config = { ...template.designConfig }
    } else if (template.id) {
      config = { template: template.id }
    }
    
    config.data = sampleData
    
    // 添加主题配色（完全对齐官网采集的实际样式）
    // 使用 base 和 item 来强制覆盖模板中的硬编码颜色
    config.themeConfig = {
      colorPrimary: themeColors.primary,
      colorBg: themeColors.background,
      palette: [themeColors.primary, themeColors.secondary, themeColors.accent],
      // 全局基础样式（官网风格：10%-40%透明度 + 细描边）
      base: {
        shape: {
          fill: themeColors.primary,
          fillOpacity: 0.1,  // 官网实际透明度 #1783ff1a = 10%
          stroke: themeColors.primary,
          strokeOpacity: 0.5,
          lineWidth: 1
        },
        text: {
          fill: themeColors.text,  // #262626
          fontSize: 13,
          fontWeight: 400
        }
      },
      // 项级样式（区块配色：20%-25%透明度，实现背景与区块差异化）
      item: {
        shape: {
          fill: themeColors.secondary,
          fillOpacity: 0.2,  // 官网实际透明度 #1783ff20 = 12.5%
          stroke: themeColors.accent,
          strokeOpacity: 0.6,
          lineWidth: 1.5
        },
        label: {
          fill: themeColors.lightText,  // #666666 官网次级文本
          fontSize: 13,
          fontWeight: 400
        },
        value: {
          fill: themeColors.primary,
          fontSize: 16,
          fontWeight: 600  // 官网数值通常更粗
        }
      }
    }
    
    // 修复 list-waterfall 的配置
    if (template.id === 'list-waterfall' && config.design && config.design.items && Array.isArray(config.design.items)) {
      config.design.item = config.design.items[0] || { type: 'simple' }
      delete config.design.items
    }
    
    // 渲染信息图（使用更大的尺寸）
    const infographic = new Infographic({
      container: container,
      width: 800,
      height: 600,
      ...config
    })
    
    infographic.render()
    console.log(`✓ 成功渲染详情预览: ${template.id}`)
  } catch (error) {
    console.error(`✗ 渲染详情预览失败: ${template.id}`, error)
    // 显示错误信息
    if (container) {
      container.innerHTML = `
        <div style="display: flex; align-items: center; justify-content: center; height: 100%; color: #ef4444;">
          <div style="text-align: center;">
            <p style="font-size: 18px; margin-bottom: 8px;">⚠️ 渲染失败</p>
            <p style="font-size: 14px; color: #6b7280;">${error instanceof Error ? error.message : '未知错误'}</p>
          </div>
        </div>
      `
    }
  }
}

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    // 加载所有模板
    const templatesRes = await getTemplates({ page: 1, pageSize: 100 })
    if (templatesRes.success && templatesRes.data) {
      templates.value = templatesRes.data.templates
      // 等待DOM更新后渲染预览
      await nextTick()
      // 再等待一个微任务确保 refs 已收集
      setTimeout(() => renderPreviews(), 100)
    }
    
    // 加载分类
    const categoriesRes = await getCategories()
    if (categoriesRes.success && categoriesRes.data) {
      categories.value = categoriesRes.data.map((cat: any) => ({
        ...cat,
        icon: categoryMap[cat.code]?.icon || '📌'
      }))
    }
  } catch (error) {
    console.error('加载数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 为不同模板生成配色方案（基于 AntV Infographic 官方配色）
const getThemeColors = (template: Template, index: number) => {
  // 定义多种配色方案（完全对齐官网实际采集的颜色值）
  const colorSchemes = [
    // 蓝色系 - #1783FF 官网主色
    {
      primary: '#1783FF',
      secondary: '#8BC1FF',    // 官网实际次级色
      accent: '#76A4D9',       // 官网实际强调色
      background: '#F0F7FF',   // 浅蓝背景
      text: '#262626',         // 官网深灰文本
      lightText: '#666666'     // 官网次级文本
    },
    // 青色系 - #00C9C9 官网主色
    {
      primary: '#00C9C9',
      secondary: '#70CAF8',    // 官网实际次级色
      accent: '#2491B3',       // 官网实际强调色
      background: '#E6FAFA',
      text: '#262626',
      lightText: '#666666'
    },
    // 橙色系 - #F0884D 官网主色
    {
      primary: '#F0884D',
      secondary: '#FFCB0E',    // 官网实际黄橙色
      accent: '#BD8F24',       // 官网实际金色
      background: '#FFF5ED',
      text: '#262626',
      lightText: '#666666'
    },
    // 紫色系 - #7863FF 官网主色
    {
      primary: '#7863FF',
      secondary: '#9A6EED',    // 官网实际深紫
      accent: '#D580FF',       // 官网实际浅紫
      background: '#F5F2FF',
      text: '#262626',
      lightText: '#666666'
    },
    // 浅紫色系 - #D580FF 官网主色
    {
      primary: '#D580FF',
      secondary: '#FF80CA',    // 官网实际粉紫
      accent: '#7863FF',       // 深紫作为强调
      background: '#FAF3FF',
      text: '#262626',
      lightText: '#666666'
    },
    // 绿色系 - #60C42D 官网主色
    {
      primary: '#60C42D',
      secondary: '#17C76F',    // 官网实际青绿
      accent: '#339900',       // 官网实际深绿
      background: '#F2FAED',
      text: '#262626',
      lightText: '#666666'
    },
    // 粉红色系 - #FF356A 官网主色
    {
      primary: '#FF356A',
      secondary: '#FF6376',    // 官网实际浅粉
      accent: '#E63C33',       // 官网实际红色
      background: '#FFF0F4',
      text: '#262626',
      lightText: '#666666'
    },
    // 黄色系 - #F3C52F 官网实际黄色
    {
      primary: '#F3C52F',
      secondary: '#FFCB0E',    // 官网实际亮黄
      accent: '#BD8F24',       // 官网实际金色
      background: '#FFFBEB',
      text: '#262626',
      lightText: '#666666'
    },
    // 玫红色系 - #E746A4 官网主色
    {
      primary: '#E746A4',
      secondary: '#FF80CA',    // 官网实际粉色
      accent: '#FF356A',       // 粉红作为强调
      background: '#FFF0F8',
      text: '#262626',
      lightText: '#666666'
    },
    // 深紫色系 - #9A6EED 官网主色
    {
      primary: '#9A6EED',
      secondary: '#D580FF',    // 官网实际浅紫
      accent: '#7863FF',       // 官网实际中紫
      background: '#F7F3FF',
      text: '#262626',
      lightText: '#666666'
    }
  ]
  
  // 根据模板类别选择配色
  const categoryColorMap: Record<string, number> = {
    'sequence': 0,  // 蓝色 - 顺序型
    'list': 5,      // 绿色 - 列表型
    'comparison': 2, // 橙色 - 对比型
    'relation': 3,   // 紫色 - 关系型
    'hierarchy': 1,  // 青色 - 层级型
    'chart': 6,      // 粉红色 - 图表型
    'quadrant': 4    // 浅紫色 - 四象限
  }
  
  // 优先根据类别选择，否则根据索引循环
  const schemeIndex = categoryColorMap[template.category] ?? (index % colorSchemes.length)
  return colorSchemes[schemeIndex]
}

// 渲染所有模板的预览
const renderPreviews = () => {
  console.log('开始渲染模板预览, 模板数:', filteredTemplates.value.length)
  console.log('Refs数量:', previewRefs.value.length)
  
  filteredTemplates.value.forEach((template, index) => {
    const container = previewRefs.value[index]
    if (container) {
      try {
        // 清空容器
        container.innerHTML = ''
        
        const sampleData = generateSampleData(template)
        // 获取该模板的主题色
        const themeColors = getThemeColors(template, index)
        
        // 构建配置对象
        let config: any = {}
        
        // 检查是否可以使用内置模板
        const builtInTemplateMap: Record<string, string> = {
          // 对比型模板映射
          'compare-binary-horizontal': 'compare-binary-horizontal-badge-card-arrow',
          'compare-binary-vs-card': 'compare-binary-horizontal-badge-card-vs',
          'compare-hierarchy-left-right': 'compare-hierarchy-left-right-circle-node-pill-badge',
          'compare-hierarchy-row': 'compare-swot',
          'comparison-two-column': 'compare-binary-horizontal-compact-card-fold',
          // 关系型模板映射
          'relation-circle': 'relation-circle-icon-badge',
          'relation-circle-connected': 'relation-circle-icon-badge',
          'relation-network': 'relation-circle-icon-badge',
          'mindmap-radial': 'relation-circle-icon-badge',
          // 列表型模板映射
          'list-column-simple': 'list-column-simple-vertical-arrow',
          'list-grid': 'list-grid-simple',
          'list-grid-icon-card': 'list-grid-badge-card',
          'list-grid-badge-card': 'list-grid-badge-card',
          'list-row': 'list-row-simple-horizontal-arrow',
          'list-row-icon-badge': 'list-row-horizontal-icon-arrow',
          'checklist': 'list-column-done-list'
          // 注意: list-waterfall, list-sector, list-sector-numbered, list-column-icon-card 使用数据库配置
        }
        
        // 如果有对应的内置模板,直接使用template参数
        if (builtInTemplateMap[template.id]) {
          config = {
            template: builtInTemplateMap[template.id]
          }
        } else if (template.designConfig) {
          // 否则使用数据库中的design配置
          config = { ...template.designConfig }
        } else if (template.id) {
          // 如果没有 designConfig,使用模板ID
          config = { template: template.id }
        }
        
        // 添加示例数据
        config.data = sampleData
        
        // 添加主题配色（完全对齐官网采集的实际样式）
        // 使用 base 和 item 来强制覆盖模板中的硬编码颜色
        config.themeConfig = {
          colorPrimary: themeColors.primary,
          colorBg: themeColors.background,
          palette: [themeColors.primary, themeColors.secondary, themeColors.accent],
          // 全局基础样式（官网风格：10%-40%透明度 + 细描边）
          base: {
            shape: {
              fill: themeColors.primary,
              fillOpacity: 0.1,  // 官网实际透明度 #1783ff1a = 10%
              stroke: themeColors.primary,
              strokeOpacity: 0.5,
              lineWidth: 1
            },
            text: {
              fill: themeColors.text,  // #262626
              fontSize: 13,
              fontWeight: 400
            }
          },
          // 项级样式（区块配色：20%-25%透明度，实现背景与区块差异化）
          item: {
            shape: {
              fill: themeColors.secondary,
              fillOpacity: 0.2,  // 官网实际透明度 #1783ff20 = 12.5%
              stroke: themeColors.accent,
              strokeOpacity: 0.6,
              lineWidth: 1.5
            },
            label: {
              fill: themeColors.lightText,  // #666666 官网次级文本
              fontSize: 13,
              fontWeight: 400
            },
            value: {
              fill: themeColors.primary,
              fontSize: 16,
              fontWeight: 600  // 官网数值通常更粗
            }
          }
        }
        
        // 修复 list-waterfall 的 items 配置：将 items 数组改为单个 item 对象
        if (template.id === 'list-waterfall' && config.design && config.design.items && Array.isArray(config.design.items)) {
          config.design.item = config.design.items[0] || { type: 'simple' }
          delete config.design.items
          console.log('=== list-waterfall 配置修复 ===', JSON.stringify(config, null, 2))
        }
        
        // 调试失败的模板
        const failingTemplates = ['compare-hierarchy-left-right', 'compare-hierarchy-row', 'relation-circle', 'relation-circle-connected', 'mindmap-radial']
        if (failingTemplates.includes(template.id)) {
          console.log(`\n=== ${template.id} 配置详情 ===`)
          console.log('designConfig:', JSON.stringify(template.designConfig, null, 2))
          console.log('sampleData:', JSON.stringify(sampleData, null, 2))
          console.log('最终config:', JSON.stringify(config, null, 2))
        }
        
        // 特别调试：记录 sequence-circular 的配置
        if (template.id === 'sequence-circular') {
          console.log('=== sequence-circular 配置详情 ===')
          console.log('template.designConfig:', JSON.stringify(template.designConfig, null, 2))
          console.log('最终 config:', JSON.stringify(config, null, 2))
        }
        
        // 特别调试：记录 sequence-circular-icon 的配置
        if (template.id === 'sequence-circular-icon') {
          console.log('=== sequence-circular-icon 配置详情 ===')
          console.log('template.designConfig:', JSON.stringify(template.designConfig, null, 2))
          console.log('修复前 config.design:', JSON.stringify(config.design, null, 2))
          console.log('最终 config:', JSON.stringify(config, null, 2))
        }
        
        const infographic = new Infographic({
          container: container,
          width: 280,
          height: 200,
          ...config
        })
        
        infographic.render()
        
        // 只记录 sequence-circular 的成功消息
        if (template.id === 'sequence-circular') {
          console.log(`✓ 成功渲染 sequence-circular`)
        }
        if (template.id === 'sequence-circular-icon') {
          console.log(`✓ 成功渲染 sequence-circular-icon`)
        }
      } catch (error) {
        // 记录所有模板的错误详情
        console.error(`✗ 渲染模板 ${template.id} 失败:`, error)
        if (error instanceof Error) {
          console.error('错误详情:', {
            message: error.message,
            stack: error.stack,
            name: error.name
          })
        }
      }
    } else {
      console.warn(`✗ 未找到容器 [${index}]: ${template.id}`)
    }
  })
}

// 生成示例数据
const generateSampleData = (template: Template) => {
  const category = template.category
  const templateId = template.id
  
  // 特殊模板的数据结构处理
  // 横向时间轴 - 需要 time 字段
  if (templateId === 'timeline-horizontal') {
    return {
      title: template.name,
      items: [
        { time: '2020', title: '起步阶段', desc: '项目启动' },
        { time: '2021', title: '发展阶段', desc: '快速成长' },
        { time: '2022', title: '扩张阶段', desc: '规模扩大' },
        { time: '2023', title: '成熟阶段', desc: '稳定运营' }
      ]
    }
  }
  
  // 里程碑时间轴 - 需要 time 字段
  if (templateId === 'sequence-timeline-milestone') {
    return {
      title: template.name,
      items: [
        { label: '第一阶段', desc: '项目启动', time: 'Q1 2023' },
        { label: '第二阶段', desc: '开发测试', time: 'Q2 2023' },
        { label: '第三阶段', desc: '上线运营', time: 'Q3 2023' },
        { label: '第四阶段', desc: '优化迭代', time: 'Q4 2023' }
      ]
    }
  }
  
  // 环形流程 - 需要更多步骤展示循环效果
  if (templateId === 'sequence-circular') {
    return {
      title: template.name,
      items: [
        { label: '计划', desc: 'Plan' },
        { label: '执行', desc: 'Do' },
        { label: '检查', desc: 'Check' },
        { label: '改进', desc: 'Act' }
      ]
    }
  }
  
  // 图标环形流程 - 需要icon字段
  if (templateId === 'sequence-circular-icon') {
    return {
      title: template.name,
      items: [
        { label: '计划', desc: 'Plan', icon: 'icon:mdi/check-circle' },
        { label: '执行', desc: 'Do', icon: 'icon:mdi/play-circle' },
        { label: '检查', desc: 'Check', icon: 'icon:mdi/magnify' },
        { label: '改进', desc: 'Act', icon: 'icon:mdi/arrow-up-circle' }
      ]
    }
  }
  
  // 上升步骤 - 体现递进关系，注意：只显示 STEP 和 label，不显示 desc
  if (templateId === 'sequence-ascending-steps') {
    return {
      title: '企业优势列表',
      desc: '展示企业在不同维度上的核心优势与表现值',
      items: [
        { label: '品牌影响力', step: 'STEP 1' },
        { label: '技术研发力', step: 'STEP 2' },
        { label: '市场增长快', step: 'STEP 3' },
        { label: '服务满意度', step: 'STEP 4' },
        { label: '数据资产全', step: 'STEP 5' },
        { label: '创新能力强', step: 'STEP 6' }
      ]
    }
  }
  
  // 图标上升步骤 - 需要icon字段和step标签，注意：只显示 STEP、icon 和 label，不显示 desc
  if (templateId === 'sequence-ascending-steps-icon') {
    return {
      title: '企业优势列表',
      desc: '展示企业在不同维度上的核心优势与表现值',
      items: [
        { label: '品牌影响力', icon: 'icon:mdi/star-circle', step: 'STEP 1' },
        { label: '技术研发力', icon: 'icon:mdi/lightbulb-on', step: 'STEP 2' },
        { label: '市场增长快', icon: 'icon:mdi/trending-up', step: 'STEP 3' },
        { label: '服务满意度', icon: 'icon:mdi/account-heart', step: 'STEP 4' },
        { label: '数据资产全', icon: 'icon:mdi/database', step: 'STEP 5' },
        { label: '创新能力强', icon: 'icon:mdi/rocket-launch', step: 'STEP 6' }
      ]
    }
  }
  
  // 蛇形步骤 - 需要更多步骤展示蛇形效果
  if (templateId === 'sequence-snake-steps' || templateId === 'sequence-color-snake-steps') {
    return {
      title: template.name,
      items: [
        { label: '步骤1', desc: '开始' },
        { label: '步骤2', desc: '进行' },
        { label: '步骤3', desc: '处理' },
        { label: '步骤4', desc: '审核' },
        { label: '步骤5', desc: '确认' },
        { label: '步骤6', desc: '完成' }
      ]
    }
  }
  
  // 折线步骤图 - 需要icon字段
  if (templateId === 'sequence-zigzag-steps-underline-text') {
    return {
      title: template.name,
      items: [
        { label: '需求分析', desc: '明确项目目标', icon: 'icon:mdi/file-document-edit' },
        { label: '方案设计', desc: '制定技术方案', icon: 'icon:mdi/pencil-ruler' },
        { label: '开发实施', desc: '编码与实现', icon: 'icon:mdi/code-braces' },
        { label: '测试验证', desc: '质量保证', icon: 'icon:mdi/test-tube' },
        { label: '上线部署', desc: '发布运维', icon: 'icon:mdi/rocket-launch' }
      ]
    }
  }
  
  // 根据分类生成不同的示例数据
  if (category === 'sequence') {
    return {
      title: template.name,
      items: [
        { label: '步骤1', desc: '描述信息' },
        { label: '步骤2', desc: '描述信息' },
        { label: '步骤3', desc: '描述信息' },
        { label: '步骤4', desc: '描述信息' }
      ]
    }
  } else if (category === 'list') {
    // 简单纵向列表
    if (templateId === 'list-column-simple') {
      return {
        title: template.name,
        items: [
          { label: '步骤1：需求分析', desc: '明确项目目标与用户需求' },
          { label: '步骤2：方案设计', desc: '制定技术方案与架构设计' },
          { label: '步骤3：开发实施', desc: '编码开发与功能实现' },
          { label: '步骤4：测试验证', desc: '全面测试确保质量' },
          { label: '步骤5：上线部署', desc: '发布上线与运维监控' }
        ]
      }
    }
    // 网格列表
    if (templateId === 'list-grid' || templateId === 'list-grid-icon-card' || templateId === 'list-grid-badge-card') {
      return {
        title: template.name,
        items: [
          { label: '产品优势1', desc: '技术领先行业标杆', icon: 'icon:mdi/trophy' },
          { label: '产品优势2', desc: '用户体验极致', icon: 'icon:mdi/account-star' },
          { label: '产品优势3', desc: '性能稳定可靠', icon: 'icon:mdi/shield-check' },
          { label: '产品优势4', desc: '成本经济高效', icon: 'icon:mdi/cash-multiple' },
          { label: '产品优势5', desc: '服务响应快速', icon: 'icon:mdi/rocket-launch' },
          { label: '产品优势6', desc: '扩展性强大', icon: 'icon:mdi/arrow-expand-all' }
        ]
      }
    }
    // 扇形列表
    if (templateId === 'list-sector' || templateId === 'list-sector-numbered') {
      return {
        title: template.name,
        items: [
          { label: '战略规划', desc: '制定长期发展战略', icon: 'icon:mdi/compass' },
          { label: '组织建设', desc: '完善团队与制度', icon: 'icon:mdi/account-group' },
          { label: '业务拓展', desc: '开拓新市场新客户', icon: 'icon:mdi/trending-up' },
          { label: '技术创新', desc: '持续研发与迭代', icon: 'icon:mdi/lightbulb-on' },
          { label: '品牌营销', desc: '提升品牌影响力', icon: 'icon:mdi/bullhorn' }
        ]
      }
    }
    // 瀑布流列表
    if (templateId === 'list-waterfall') {
      return {
        title: template.name,
        items: [
          { label: '需求调研', desc: '深入了解用户需求与痛点' },
          { label: '竞品分析', desc: '研究市场现状与竞争态势' },
          { label: '功能规划', desc: '梳理产品功能与优先级' },
          { label: '原型设计', desc: '设计交互原型与视觉稿' },
          { label: '技术选型', desc: '确定技术栈与架构方案' },
          { label: '开发排期', desc: '制定开发计划与里程碑' }
        ]
      }
    }
    // 纵向图标卡片列表
    if (templateId === 'list-column-icon-card') {
      return {
        title: template.name,
        items: [
          { label: '云计算服务', desc: '弹性可扩展的云端资源', icon: 'icon:mdi/cloud' },
          { label: 'AI智能', desc: '前沿人工智能技术', icon: 'icon:mdi/brain' },
          { label: '大数据分析', desc: '海量数据处理能力', icon: 'icon:mdi/chart-bar' },
          { label: '物联网', desc: '万物互联智能硬件', icon: 'icon:mdi/wifi' },
          { label: '区块链', desc: '去中心化可信技术', icon: 'icon:mdi/lock-outline' }
        ]
      }
    }
    // 检查清单
    if (templateId === 'checklist') {
      return {
        title: template.name,
        items: [
          { label: '完成需求文档编写', desc: '已完成', done: true },
          { label: '完成技术方案评审', desc: '已完成', done: true },
          { label: '完成原型设计确认', desc: '已完成', done: true },
          { label: '开发环境搭建完成', desc: '进行中', done: false },
          { label: '核心功能开发', desc: '待开始', done: false }
        ]
      }
    }
    // 横向列表（包含图标箭头）- 需要 icon、value、time、illus 字段
    if (templateId === 'list-row-horizontal-icon-arrow') {
      return {
        title: '企业优势列表',
        desc: '展示企业在不同维度上的核心优势与表现值',
        items: [
          {
            icon: 'icon:mdi/diamond-stone',
            label: '品牌影响力',
            desc: '在目标用户群中具备较强认知与信任度',
            value: 85,
            time: '2021',
            illus: 'illus:creative-experiment'
          },
          {
            icon: 'icon:mdi/code-braces',
            label: '技术研发力',
            desc: '拥有自研核心系统与持续创新能力',
            value: 90,
            time: '2022',
            illus: 'illus:code-thinking'
          },
          {
            icon: 'icon:mdi/wallet',
            label: '市场增长快',
            desc: '近一年用户规模实现快速增长',
            value: 78,
            time: '2023',
            illus: 'illus:business-analytics'
          },
          {
            icon: 'icon:mdi/emoticon-happy',
            label: '服务满意度',
            desc: '用户对服务体系整体评分较高',
            value: 88,
            time: '2020',
            illus: 'illus:feeling-happy'
          },
          {
            icon: 'icon:mdi/account-circle',
            label: '数据资产全',
            desc: '构建了完整用户标签与画像体系',
            value: 92,
            time: '2022',
            illus: 'illus:mobile-photos'
          },
          {
            icon: 'icon:mdi/rocket-launch',
            label: '创新能力强',
            desc: '新产品上线频率高于行业平均',
            value: 83,
            time: '2023',
            illus: 'illus:creativity'
          }
        ]
      }
    }
    // 横向列表（普通）
    if (templateId === 'list-row' || templateId === 'list-row-icon-badge') {
      return {
        title: template.name,
        items: [
          { label: '规划', desc: 'Plan', icon: 'icon:mdi/clipboard-text' },
          { label: '执行', desc: 'Do', icon: 'icon:mdi/play-circle' },
          { label: '检查', desc: 'Check', icon: 'icon:mdi/magnify' },
          { label: '改进', desc: 'Act', icon: 'icon:mdi/arrow-up-circle' }
        ]
      }
    }
    // 默认列表型数据
    return {
      title: template.name,
      items: [
        { label: '项目1', desc: '示例描述', icon: 'icon:mdi/check-circle' },
        { label: '项目2', desc: '示例描述', icon: 'icon:mdi/star' },
        { label: '项目3', desc: '示例描述', icon: 'icon:mdi/heart' },
        { label: '项目4', desc: '示例描述', icon: 'icon:mdi/thumb-up' }
      ]
    }
  } else if (category === 'comparison') {
    // 横向二元对比 - 使用左右数组结构
    if (templateId === 'compare-binary-horizontal') {
      return {
        title: template.name,
        desc: '快速对比两种方案的优劣差异',
        items: [
          [
            { label: '产品研发能力强', desc: '持续创新，技术领先' },
            { label: '客户满意度高', desc: '服务体验优质，复购率高' },
            { label: '品牌影响力大', desc: '市场认知度广，口碑良好' }
          ],
          [
            { label: '市场渠道较窄', desc: '线下覆盖不足，需扩展' },
            { label: '运营成本偏高', desc: '人力与物流成本待优化' },
            { label: '产品线单一', desc: '品类不够丰富，需拓展' }
          ]
        ]
      }
    }
    // VS对比卡片 - 带VS标识的二元对比
    if (templateId === 'compare-binary-vs-card') {
      return {
        title: template.name,
        desc: '产品或方案的直接PK对比',
        items: [
          [
            { label: '方案A优势1', desc: '成本低，易实施' },
            { label: '方案A优势2', desc: '风险可控，稳定性好' },
            { label: '方案A优势3', desc: '团队熟悉，上手快' }
          ],
          [
            { label: '方案B优势1', desc: '效果显著，收益高' },
            { label: '方案B优势2', desc: '技术先进，扩展性强' },
            { label: '方案B优势3', desc: '用户体验佳，满意度高' }
          ]
        ]
      }
    }
    // 左右对比需要层级数据结构
    if (templateId === 'compare-hierarchy-left-right') {
      return {
        title: template.name,
        desc: '呈现企业当前在市场中的核心优势与待改善劣势',
        items: [
          {
            label: '优势',
            children: [
              { label: '产品研发强', desc: '技术领先，具备自主创新能力' },
              { label: '客户粘性高', desc: '用户复购率超60%，口碑良好' },
              { label: '服务体系完善', desc: '售后服务响应快，客户满意度高' }
            ]
          },
          {
            label: '劣势',
            children: [
              { label: '品牌曝光弱', desc: '市场宣传不足，认知度待提升' },
              { label: '渠道覆盖窄', desc: '线上渠道布局不全，触达受限' },
              { label: '运营成本高', desc: '人力与物流成本高于行业均值' }
            ]
          }
        ]
      }
    }
    // SWOT分析 - 4象限对比
    if (templateId === 'compare-hierarchy-row' || templateId === 'swot-analysis') {
      return {
        title: 'SWOT分析',
        desc: '通过全面分析内外部因素，指导企业战略制定与调整',
        items: [
          {
            label: 'Strengths',
            children: [
              { label: '领先的技术研发能力' },
              { label: '完善的供应链体系' },
              { label: '高效的客户服务机制' },
              { label: '成熟的管理团队' },
              { label: '良好的用户口碑' },
              { label: '稳定的产品质量' }
            ]
          },
          {
            label: 'Weaknesses',
            children: [
              { label: '品牌曝光度不足' },
              { label: '产品线更新缓慢' },
              { label: '市场渠道单一' },
              { label: '运营成本较高' },
              { label: '组织决策效率偏低' },
              { label: '用户增长放缓' }
            ]
          },
          {
            label: 'Opportunities',
            children: [
              { label: '数字化转型趋势加速' },
              { label: '新兴市场持续扩展' },
              { label: '政策利好推动行业发展' },
              { label: '智能化应用场景增加' },
              { label: '跨界合作机会增多' },
              { label: '用户消费升级趋势' }
            ]
          },
          {
            label: 'Threats',
            children: [
              { label: '行业竞争日益激烈' },
              { label: '用户需求快速变化' },
              { label: '市场进入门槛降低' },
              { label: '供应链风险上升' },
              { label: '数据与安全挑战加剧' },
              { label: '宏观经济不确定性' }
            ]
          }
        ]
      }
    }
    // 双栏对比 - 简单的左右对比
    if (templateId === 'comparison-two-column') {
      return {
        title: template.name,
        desc: '简洁的双栏对比布局',
        items: [
          [
            { label: '优势项1', desc: '描述信息' },
            { label: '优势项2', desc: '描述信息' },
            { label: '优势项3', desc: '描述信息' }
          ],
          [
            { label: '劣势项1', desc: '描述信息' },
            { label: '劣势项2', desc: '描述信息' },
            { label: '劣势项3', desc: '描述信息' }
          ]
        ]
      }
    }
    // 默认对比型数据
    return {
      title: template.name,
      items: [
        [
          { label: '选项A特点1', desc: '描述' },
          { label: '选项A特点2', desc: '描述' },
          { label: '选项A特点3', desc: '描述' }
        ],
        [
          { label: '选项B特点1', desc: '描述' },
          { label: '选项B特点2', desc: '描述' },
          { label: '选项B特点3', desc: '描述' }
        ]
      ]
    }
  } else if (category === 'chart') {
    return {
      title: template.name,
      items: [
        { label: 'Q1', value: 100 },
        { label: 'Q2', value: 120 },
        { label: 'Q3', value: 90 },
        { label: 'Q4', value: 140 }
      ]
    }
  } else if (category === 'hierarchy') {
    // 组织架构需要树形数据结构
    if (templateId === 'org-tree' || templateId.includes('hierarchy-tree')) {
      return {
        title: template.name,
        items: [
          {
            label: 'CEO',
            desc: '首席执行官',
            children: [
              {
                label: 'CTO',
                desc: '技术总监',
                children: [
                  { label: '开发组', desc: '软件研发' },
                  { label: '测试组', desc: '质量保证' }
                ]
              },
              {
                label: 'COO',
                desc: '运营总监',
                children: [
                  { label: '市场部', desc: '市场营销' },
                  { label: '销售部', desc: '业务拓展' }
                ]
              }
            ]
          }
        ]
      }
    }
    return {
      title: template.name,
      items: [
        { label: '高层', desc: '描述' },
        { label: '中层', desc: '描述' },
        { label: '基层', desc: '描述' }
      ]
    }
  } else if (category === 'relation') {
    // 环形关系图 - 使用icon-badge样式
    if (templateId === 'relation-circle') {
      return {
        title: '子公司盈利分析',
        desc: '各子公司财务表现，盈利同比增长',
        items: [
          { label: '云计算子公司', value: 25, icon: 'icon:mdi/cloud' },
          { label: '人工智能子公司', value: 40, icon: 'icon:mdi/brain' },
          { label: '物联网子公司', value: 30, icon: 'icon:mdi/wifi' },
          { label: '金融科技子公司', value: 18, icon: 'icon:mdi/currency-usd' },
          { label: '新能源子公司', value: 50, icon: 'icon:mdi/battery-charging' }
        ]
      }
    }
    // 连线环形关系图
    if (templateId === 'relation-circle-connected') {
      return {
        title: '产品生态圈',
        desc: '核心产品与配套服务的关系网络',
        items: [
          { label: '核心产品', value: 50, icon: 'icon:mdi/star' },
          { label: '技术支持', value: 30, icon: 'icon:mdi/tools' },
          { label: '运营服务', value: 35, icon: 'icon:mdi/cog' },
          { label: '数据分析', value: 40, icon: 'icon:mdi/chart-bar' },
          { label: '客户支持', value: 28, icon: 'icon:mdi/message-text' }
        ]
      }
    }
    // 网络关系图
    if (templateId === 'relation-network') {
      return {
        title: '企业合作网络',
        desc: '主要合作伙伴与业务关系',
        items: [
          { label: '核心企业', value: 60, icon: 'icon:mdi/office-building' },
          { label: '供应商A', value: 35, icon: 'icon:mdi/truck-delivery' },
          { label: '供应商B', value: 30, icon: 'icon:mdi/package-variant' },
          { label: '渠道商A', value: 40, icon: 'icon:mdi/store' },
          { label: '渠道商B', value: 38, icon: 'icon:mdi/shopping' },
          { label: '技术伙伴', value: 42, icon: 'icon:mdi/code-tags' }
        ]
      }
    }
    // 放射状思维导图
    if (templateId === 'mindmap-radial') {
      return {
        title: '企业核心能力',
        desc: '核心竞争力要素分析',
        items: [
          { label: '技术创新', value: 45, icon: 'icon:mdi/lightbulb-on' },
          { label: '品牌价值', value: 38, icon: 'icon:mdi/medal' },
          { label: '团队实力', value: 42, icon: 'icon:mdi/account-group' },
          { label: '运营效率', value: 40, icon: 'icon:mdi/rocket-launch' },
          { label: '客户资源', value: 35, icon: 'icon:mdi/account-star' },
          { label: '资金实力', value: 48, icon: 'icon:mdi/cash-multiple' }
        ]
      }
    }
    // 默认关系型数据
    return {
      title: template.name,
      items: [
        { label: '节点1', value: 30, icon: 'icon:mdi/check-circle' },
        { label: '节点2', value: 40, icon: 'icon:mdi/star' },
        { label: '节点3', value: 35, icon: 'icon:mdi/heart' },
        { label: '节点4', value: 25, icon: 'icon:mdi/thumb-up' }
      ]
    }
  } else if (category === 'quadrant') {
    // 四象限使用简单的 items 数组,固定4个元素
    if (templateId === 'swot-analysis' || templateId === 'quadrant-priority-matrix' || templateId.includes('quadrant')) {
      return {
        title: template.name,
        items: [
          { label: '象限1', desc: '右上角' },
          { label: '象限2', desc: '左上角' },
          { label: '象限3', desc: '左下角' },
          { label: '象限4', desc: '右下角' }
        ]
      }
    }
    return {
      title: template.name,
      quadrants: [
        { title: '象限1', items: ['A', 'B'] },
        { title: '象限2', items: ['C', 'D'] },
        { title: '象限3', items: ['E', 'F'] },
        { title: '象限4', items: ['G', 'H'] }
      ]
    }
  }
  
  return {
    title: template.name,
    items: [
      { label: '示例1' },
      { label: '示例2' },
      { label: '示例3' }
    ]
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped lang="scss">
.examples-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f9fafb;
}

.examples-main {
  flex: 1;
  overflow-y: auto;
  padding: 2rem 1rem;
}

.examples-container {
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 2rem;
  text-align: center;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.page-subtitle {
  font-size: 1.125rem;
  color: #6b7280;
}

.category-filter {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  justify-content: center;
}

.filter-button {
  padding: 0.625rem 1.25rem;
  border: 1px solid #e5e7eb;
  background: white;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
  
  &:hover {
    border-color: #3b82f6;
    color: #3b82f6;
  }
  
  &.active {
    background: #3b82f6;
    color: white;
    border-color: #3b82f6;
  }
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e5e7eb;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text {
  margin-top: 1rem;
  color: #6b7280;
  font-size: 0.875rem;
}

.templates-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.template-card {
  position: relative;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 0;
  cursor: pointer;
  transition: all 0.3s;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  
  &:hover {
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);
    
    .card-overlay {
      opacity: 1;
    }
  }
}

.card-preview {
  width: 100%;
  height: 200px;
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.preview-canvas {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  
  :deep(svg) {
    max-width: 100%;
    max-height: 100%;
  }
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
  padding: 1rem 1.5rem 0 1.5rem;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
}

.card-badge {
  padding: 0.25rem 0.625rem;
  background: #eff6ff;
  color: #3b82f6;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 500;
  white-space: nowrap;
}

.card-description {
  color: #6b7280;
  font-size: 0.875rem;
  line-height: 1.5;
  margin-bottom: 1rem;
  padding: 0 1.5rem;
}

.card-footer {
  margin-top: auto;
  padding: 0 1.5rem 1.5rem 1.5rem;
}

.card-tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.tag {
  padding: 0.25rem 0.5rem;
  background: #f3f4f6;
  color: #6b7280;
  border-radius: 4px;
  font-size: 0.75rem;
}

.card-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(59, 130, 246, 0.95);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.overlay-content {
  text-align: center;
}

.preview-button {
  padding: 0.75rem 1.5rem;
  background: white;
  color: #3b82f6;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  
  &:hover {
    transform: scale(1.05);
  }
}

.empty-state {
  padding: 4rem;
  text-align: center;
}

.empty-text {
  color: #9ca3af;
  font-size: 1rem;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 16px;
  max-width: 900px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
}

.close-button {
  background: none;
  border: none;
  cursor: pointer;
  color: #6b7280;
  padding: 0.5rem;
  border-radius: 8px;
  transition: all 0.2s;
  
  &:hover {
    background: #f3f4f6;
    color: #1f2937;
  }
}

.modal-body {
  padding: 2rem;
}

.template-info {
  margin-bottom: 2rem;
}

.info-row {
  display: flex;
  margin-bottom: 1rem;
  
  &:last-child {
    margin-bottom: 0;
  }
}

.info-label {
  font-weight: 600;
  color: #374151;
  min-width: 100px;
}

.info-value {
  color: #6b7280;
  flex: 1;
}

.info-tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  flex: 1;
}

.info-tag {
  padding: 0.25rem 0.75rem;
  background: #eff6ff;
  color: #3b82f6;
  border-radius: 6px;
  font-size: 0.875rem;
}

.template-preview {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 2rem;
  min-height: 600px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.detail-preview-canvas {
  width: 100%;
  height: 100%;
  min-height: 600px;
  display: flex;
  align-items: center;
  justify-content: center;
  
  :deep(svg) {
    max-width: 100%;
    max-height: 100%;
  }
}
</style>
