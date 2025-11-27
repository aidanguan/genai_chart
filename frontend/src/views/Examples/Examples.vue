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
            <div class="preview-placeholder">
              <p class="placeholder-text">信息图预览区域</p>
              <p class="placeholder-hint">模板ID: {{ selectedTemplate.id }}</p>
            </div>
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
}

const closePreview = () => {
  selectedTemplate.value = null
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
        
        // 构建配置对象
        let config: any = {}
        
        if (template.designConfig) {
          config = { ...template.designConfig }
          
          // 修复 item 类型：把不支持的 item 类型替换为支持的类型
          if (config.design?.item === 'icon-card') {
            config.design.item = 'icon'
          }
          
          // 修复：如果 design 对象为空，根据模板ID补全配置
          if (config.design && Object.keys(config.design).length === 0) {
            // sequence-circular 相关模板
            if (template.id === 'sequence-circular') {
              config.design = {
                structure: { type: 'sequence-circular' },
                title: 'default',
                item: 'simple'
              }
            } else if (template.id === 'sequence-circular-icon') {
              config.design = {
                structure: { type: 'sequence-circular' },
                title: 'default',
                item: 'icon'  // 修复：使用 'icon' 而不是 'icon-card'
              }
            }
            // timeline 相关模板
            else if (template.id === 'timeline-horizontal') {
              config.design = {
                structure: { type: 'timeline-horizontal' },
                title: 'default',
                item: 'simple'
              }
            } else if (template.id === 'sequence-timeline-milestone') {
              config.design = {
                structure: { type: 'sequence-timeline' },
                title: 'default',
                item: 'milestone-card'
              }
            }
            // 其他使用 design 对象的模板，尝试从 structure_type 构建
            else if (template.id) {
              const structureType = template.id.replace(/-icon$/, '')
              config.design = {
                structure: { type: structureType },
                title: 'default',
                item: template.id.includes('-icon') ? 'icon' : 'simple'
              }
            }
          }
        } else if (template.id) {
          // 否则直接使用模板ID
          config = { template: template.id }
        }
        
        // 添加示例数据
        config.data = sampleData
        
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
        // 特别记录 sequence-circular-icon 的错误
        if (template.id === 'sequence-circular-icon') {
          console.error(`✗ 渲染模板 ${template.id} 失败:`, error)
          if (error instanceof Error) {
            console.error('错误详情:', error.message, error.stack)
          }
        } else {
          console.error(`✗ 渲染模板 ${template.id} 失败:`, error)
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
  
  // 上升步骤 - 体现递进关系
  if (templateId === 'sequence-ascending-steps') {
    return {
      title: template.name,
      items: [
        { label: '初级', desc: '基础入门' },
        { label: '中级', desc: '进阶提升' },
        { label: '高级', desc: '专业精通' },
        { label: '专家', desc: '行业领先' }
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
    return {
      title: template.name,
      items: [
        { label: '项目1', desc: '示例描述' },
        { label: '项目2', desc: '示例描述' },
        { label: '项目3', desc: '示例描述' },
        { label: '项目4', desc: '示例描述' }
      ]
    }
  } else if (category === 'comparison') {
    return {
      title: template.name,
      left: {
        title: '选项A',
        items: ['特点1', '特点2', '特点3']
      },
      right: {
        title: '选项B',
        items: ['特点1', '特点2', '特点3']
      }
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
    return {
      title: template.name,
      items: [
        { label: '高层', desc: '描述' },
        { label: '中层', desc: '描述' },
        { label: '基层', desc: '描述' }
      ]
    }
  } else if (category === 'relation') {
    return {
      title: template.name,
      center: '核心',
      nodes: [
        { label: '节点1' },
        { label: '节点2' },
        { label: '节点3' },
        { label: '节点4' }
      ]
    }
  } else if (category === 'quadrant') {
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
  padding: 3rem;
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.preview-placeholder {
  text-align: center;
}

.placeholder-text {
  font-size: 1.125rem;
  color: #6b7280;
  margin-bottom: 0.5rem;
}

.placeholder-hint {
  font-size: 0.875rem;
  color: #9ca3af;
}
</style>
