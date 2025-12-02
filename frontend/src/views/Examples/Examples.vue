<template>
  <div class="examples-page">
    <!-- Header -->
    <WorkspaceHeader />
    
    <!-- Main Content -->
    <main class="examples-main">
      <div class="examples-container">
        <!-- 页面标题 -->
        <div class="page-header">
          <h1 class="page-title">用户作品示例</h1>
          <p class="page-subtitle">浏览用户分享的信息图作品，共 {{ totalCount }} 个作品</p>
        </div>
        
        <!-- 类型筛选 -->
        <div class="category-filter">
          <button 
            class="filter-button" 
            :class="{ active: selectedCategory === '' }"
            @click="selectedCategory = ''"
          >
            全部 ({{ works.length }})
          </button>
          <button 
            v-for="cat in categories"
            :key="cat.code"
            class="filter-button"
            :class="{ active: selectedCategory === cat.code }"
            @click="selectedCategory = cat.code"
          >
            {{ cat.name }} ({{ works.filter(w => templates.get(w.templateId)?.category === cat.code).length }})
          </button>
        </div>
        
        <!-- 加载状态 -->
        <div v-if="loading" class="loading-container">
          <div class="loading-spinner"></div>
          <p class="loading-text">加载中...</p>
        </div>
        
        <!-- 作品网格 -->
        <div v-else class="templates-grid">
          <div 
            v-for="(work, index) in filteredWorks"
            :key="work.id"
            class="template-card"
            @click="handleWorkClick(work)"
          >
            <!-- 预览区域 -->
            <div class="card-preview">
              <div :ref="el => setPreviewRef(el, index)" class="preview-canvas"></div>
            </div>
            
            <div class="card-header">
              <h3 class="card-title">{{ work.title || '信息图作品' }}</h3>
              <span class="card-badge">{{ getCategoryName(work.templateId) }}</span>
            </div>
            <p class="card-description">{{ getWorkDescription(work) }}</p>
            <div class="card-footer">
              <div class="card-tags">
                <span class="tag tag-template">
                  {{ getTemplateName(work.templateId) }}
                </span>
                <span class="tag">
                  {{ formatDate(work.createdAt) }}
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
        <div v-if="!loading && filteredWorks.length === 0" class="empty-state">
          <p class="empty-text">{{ selectedCategory ? '该分类暂无作品' : '暂无用户分享的作品' }}</p>
        </div>
      </div>
    </main>
    
    <!-- 作品预览弹窗 -->
    <div v-if="selectedWork" class="modal-overlay" @click.self="closePreview">
      <div class="modal-content">
        <div class="modal-header">
          <h2 class="modal-title">{{ selectedWork?.title || '信息图作品' }}</h2>
          <div class="header-actions">
            <button class="action-button" @click="handleViewCode" title="查看代码">
              <Code2 :size="20" />
            </button>
            <button class="action-button action-delete" @click="(e) => selectedWork && handleDelete(selectedWork, e)" title="删除作品">
              <Trash2 :size="20" />
            </button>
            <button class="close-button" @click="closePreview">
              <X :size="24" />
            </button>
          </div>
        </div>
        <div class="modal-body">
          <div class="template-info">
            <div class="info-row">
              <span class="info-label">模板名称：</span>
              <span class="info-value">{{ selectedWork ? getTemplateName(selectedWork.templateId) : '-' }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">模板类型：</span>
              <span class="info-value">{{ selectedWork ? getCategoryName(selectedWork.templateId) : '-' }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">创建时间：</span>
              <span class="info-value">{{ selectedWork?.createdAt ? formatDate(selectedWork.createdAt) : '-' }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">原始文本：</span>
              <span class="info-value">{{ selectedWork?.inputText || '-' }}</span>
            </div>
          </div>
          <div class="template-preview">
            <div ref="detailPreviewRef" class="detail-preview-canvas"></div>
          </div>
          
          <!-- 代码查看器 -->
          <div v-if="showCodeViewer" class="code-viewer">
            <div class="code-header">
              <h3 class="code-title">信息图配置</h3>
              <button class="copy-button" @click="handleCopyCode">复制代码</button>
            </div>
            <pre class="code-content"><code>{{ codeContent }}</code></pre>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { X, Trash2, Code2 } from 'lucide-vue-next'
import WorkspaceHeader from '@/views/AIWorkspace/components/WorkspaceHeader.vue'
import { getWorks, deleteWork } from '@/api/work'
import { templateAPI } from '@/api/templates'
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

interface UserWork {
  id: number
  title: string
  templateId: string
  inputText: string
  infographicConfig: any
  createdAt: string
  updatedAt: string
}

interface TemplateInfo {
  id: string
  name: string
  category: string
}

interface Category {
  code: string
  name: string
  description: string
  count: number
}

// 状态
const loading = ref(false)
const works = ref<UserWork[]>([])
const selectedWork = ref<UserWork | null>(null)
const previewRefs = ref<(HTMLElement | null)[]>([])
const detailPreviewRef = ref<HTMLElement | null>(null)
const templates = ref<Map<string, TemplateInfo>>(new Map())
const categories = ref<Category[]>([])
const selectedCategory = ref<string>('')
const showCodeViewer = ref(false)
const codeContent = ref('')

// 计算属性
const totalCount = computed(() => filteredWorks.value.length)

// 分类映射
const categoryMap: Record<string, string> = {
  chart: '图表型',
  comparison: '对比型',
  hierarchy: '层级型',
  list: '列表型',
  quadrant: '四象限型',
  relation: '关系型',
  sequence: '顺序型'
}

// 过滤后的作品列表
const filteredWorks = computed(() => {
  if (!selectedCategory.value) {
    return works.value
  }
  return works.value.filter(work => {
    const template = templates.value.get(work.templateId)
    return template && template.category === selectedCategory.value
  })
})

// 方法
const setPreviewRef = (el: any, index: number) => {
  if (el) {
    previewRefs.value[index] = el as HTMLElement
  }
}

const getWorkDescription = (work: UserWork) => {
  const text = work.inputText
  return text.length > 100 ? text.substring(0, 100) + '...' : text
}

const getTemplateName = (templateId: string) => {
  return templates.value.get(templateId)?.name || '未知模板'
}

const getCategoryName = (templateId: string) => {
  const template = templates.value.get(templateId)
  if (!template) return '未知类型'
  return categoryMap[template.category] || template.category
}

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', { 
    year: 'numeric', 
    month: '2-digit', 
    day: '2-digit' 
  })
}

const handleWorkClick = (work: UserWork) => {
  selectedWork.value = work
  // 等待弹窗 DOM 渲染后再渲染信息图
  nextTick(() => {
    setTimeout(() => renderDetailPreview(work), 50)
  })
}

const closePreview = () => {
  selectedWork.value = null
  showCodeViewer.value = false
  // 清空详情预览容器
  if (detailPreviewRef.value) {
    detailPreviewRef.value.innerHTML = ''
  }
}

// 删除作品
const handleDelete = async (work: UserWork, event: Event) => {
  event.stopPropagation() // 阻止冒泡
  
  if (!confirm(`确定要删除作品 "${work.title || '信息图作品'}" 吗？`)) {
    return
  }
  
  try {
    const result = await deleteWork(work.id)
    if (result.success) {
      // 从列表中移除
      works.value = works.value.filter(w => w.id !== work.id)
      // 如果当前正在查看被删除的作品，关闭弹窗
      if (selectedWork.value?.id === work.id) {
        closePreview()
      }
      alert('删除成功')
    } else {
      alert('删除失败：' + (result.message || '未知错误'))
    }
  } catch (error) {
    console.error('删除作品失败:', error)
    alert('删除失败，请稍后重试')
  }
}

// 查看代码
const handleViewCode = (event: Event) => {
  event.stopPropagation()
  if (selectedWork.value) {
    codeContent.value = JSON.stringify(selectedWork.value.infographicConfig, null, 2)
    showCodeViewer.value = true
  }
}

// 复制代码
const handleCopyCode = async () => {
  try {
    await navigator.clipboard.writeText(codeContent.value)
    alert('代码已复制到剪贴板')
  } catch (error) {
    console.error('复制失败:', error)
    alert('复制失败，请手动复制')
  }
}

// 渲染详情弹窗中的信息图
const renderDetailPreview = (work: UserWork) => {
  const container = detailPreviewRef.value
  if (!container) {
    console.warn('详情预览容器未找到')
    return
  }
  
  try {
    // 清空容器
    container.innerHTML = ''
    
    // 直接使用作品的配置
    const config = work.infographicConfig
    
    // 渲染信息图（使用更大的尺寸）
    const infographic = new Infographic({
      container: container,
      width: 800,
      height: 600,
      ...config
    })
    
    infographic.render()
    console.log(`✓ 成功渲染作品详情: ${work.id}`)
  } catch (error) {
    console.error(`✗ 渲染作品详情失败: ${work.id}`, error)
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
    // 并行加载作品列表和分类信息
    const [worksRes, categoriesRes] = await Promise.all([
      getWorks(1, 100),
      templateAPI.getCategories()
    ])
    
    if (worksRes.success && worksRes.data) {
      works.value = worksRes.data.works
      
      // 提取所有唯一的templateId
      const templateIds = [...new Set(works.value.map(w => w.templateId))]
      
      console.log('[Examples] 需要加载的模板:', templateIds)
      
      // 使用精确查询加载每个模板的详情
      const templatePromises = templateIds.map(id => 
        templateAPI.getTemplate(id)
          .then(res => res.success && res.data ? res.data : null)
          .catch(err => {
            console.error(`加载模板 ${id} 失败:`, err)
            return null
          })
      )
      const templateResults = await Promise.all(templatePromises)
      
      // 构建模板映射表
      const templateMap = new Map<string, TemplateInfo>()
      templateResults.forEach(template => {
        if (template) {
          templateMap.set(template.id, {
            id: template.id,
            name: template.name,
            category: template.category
          })
          console.log(`✓ 加载模板: ${template.id} - ${template.name} (${template.category})`)
        }
      })
      templates.value = templateMap
      
      console.log('[Examples] 模板映射表大小:', templateMap.size)
      
      // 等待DOM更新后渲染预览
      await nextTick()
      setTimeout(() => renderPreviews(), 100)
    }
    
    if (categoriesRes.success && categoriesRes.data) {
      categories.value = categoriesRes.data
    }
  } catch (error) {
    console.error('加载数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 渲染所有用户作品的预览
const renderPreviews = () => {
  console.log('开始渲染用户作品预览, 作品数:', filteredWorks.value.length)
  console.log('Refs数量:', previewRefs.value.length)
  
  filteredWorks.value.forEach((work, index) => {
    const container = previewRefs.value[index]
    if (container) {
      try {
        // 清空容器
        container.innerHTML = ''
        
        // 直接使用作品的配置
        const config = work.infographicConfig
        
        const infographic = new Infographic({
          container: container,
          width: 280,
          height: 200,
          ...config
        })
        
        infographic.render()
        console.log(`✓ 成功渲染作品: ${work.id}`)
      } catch (error) {
        console.error(`✗ 渲染作品 ${work.id} 失败:`, error)
        if (error instanceof Error) {
          console.error('错误详情:', {
            message: error.message,
            stack: error.stack,
            name: error.name
          })
        }
      }
    } else {
      console.warn(`✗ 未找到容器 [${index}]: ${work.id}`)
    }
  })
}

onMounted(() => {
  loadData()
})

// 监听分类筛选变化，重新渲染预览
watch(selectedCategory, () => {
  nextTick(() => {
    setTimeout(() => renderPreviews(), 100)
  })
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
  
  &.tag-template {
    background: #dbeafe;
    color: #1e40af;
    font-weight: 500;
  }
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

.header-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.action-button {
  background: none;
  border: none;
  cursor: pointer;
  color: #3b82f6;
  padding: 0.5rem;
  border-radius: 8px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  
  &:hover {
    background: #eff6ff;
    color: #2563eb;
  }
  
  &.action-delete {
    color: #ef4444;
    
    &:hover {
      background: #fee2e2;
      color: #dc2626;
    }
  }
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

.code-viewer {
  margin-top: 2rem;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
}

.code-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

.code-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.copy-button {
  padding: 0.5rem 1rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  
  &:hover {
    background: #2563eb;
  }
  
  &:active {
    transform: scale(0.98);
  }
}

.code-content {
  margin: 0;
  padding: 1.5rem;
  background: #1f2937;
  color: #e5e7eb;
  font-family: 'Courier New', Courier, monospace;
  font-size: 0.875rem;
  line-height: 1.6;
  overflow-x: auto;
  max-height: 500px;
  overflow-y: auto;
  
  code {
    color: #e5e7eb;
  }
}
</style>
