<template>
  <a-modal
    v-model:open="visible"
    title="选择信息图模板"
    width="800px"
    :footer="null"
    :maskClosable="true"
    @cancel="handleClose"
  >
    <div class="template-modal-content">
      <!-- 搜索和筛选 -->
      <div class="search-bar">
        <a-input
          v-model:value="searchKeyword"
          placeholder="搜索模板名称或描述..."
          allow-clear
        >
          <template #prefix>
            <Search :size="16" />
          </template>
        </a-input>
      </div>
      
      <!-- 分类标签 -->
      <div class="category-tabs">
        <a-radio-group v-model:value="selectedCategory" button-style="solid">
          <a-radio-button value="">全部</a-radio-button>
          <a-radio-button
            v-for="cat in categories"
            :key="cat.code"
            :value="cat.code"
          >
            {{ cat.name }} ({{ cat.count }})
          </a-radio-button>
        </a-radio-group>
      </div>
      
      <!-- 模板网格 -->
      <div class="template-grid">
        <div
          v-for="template in filteredTemplates"
          :key="template.id"
          class="template-item"
          @click="handleTemplateSelect(template.id)"
        >
          <div class="template-card">
            <!-- 分类标签 -->
            <div class="category-badge">{{ getCategoryName(template.category) }}</div>
            
            <!-- 模板内容 -->
            <div class="template-info">
              <div class="template-name">{{ template.name }}</div>
              <div class="template-desc">{{ template.description || template.useCases }}</div>
            </div>
            
            <!-- 标签 -->
            <div class="template-tags" v-if="template.tags && template.tags.length > 0">
              <span
                v-for="tag in template.tags.slice(0, 3)"
                :key="tag"
                class="tag"
              >
                {{ tag }}
              </span>
            </div>
          </div>
        </div>
        
        <!-- 空状态 -->
        <div v-if="filteredTemplates.length === 0" class="empty-result">
          <FileX :size="48" />
          <p>未找到匹配的模板</p>
        </div>
      </div>
    </div>
  </a-modal>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { Modal as AModal, Input as AInput, RadioGroup as ARadioGroup, RadioButton as ARadioButton } from 'ant-design-vue'
import { Search, FileX } from 'lucide-vue-next'
import { message } from 'ant-design-vue'
import { useWorkspaceStore } from '@/stores/workspace'
import { useTemplateStore } from '@/stores/template'
import { useSettingsStore } from '@/stores/settings'

interface Props {
  modelValue: boolean
}

const props = defineProps<Props>()
const emit = defineEmits(['update:modelValue'])

const workspaceStore = useWorkspaceStore()
const templateStore = useTemplateStore()
const settingsStore = useSettingsStore()

const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const searchKeyword = ref('')
const selectedCategory = ref('')
const categories = ref<any[]>([])
const templates = ref<any[]>([])

// 分类名称映射
const categoryMap: Record<string, string> = {
  chart: '图表型',
  comparison: '对比型',
  hierarchy: '层级型',
  list: '列表型',
  quadrant: '四象限型',
  relation: '关系型',
  sequence: '顺序型'
}

function getCategoryName(category: string): string {
  return categoryMap[category] || category
}

// 过滤模板
const filteredTemplates = computed(() => {
  let result = templates.value
  
  // 按分类筛选
  if (selectedCategory.value) {
    result = result.filter(t => t.category === selectedCategory.value)
  }
  
  // 按关键词搜索
  if (searchKeyword.value.trim()) {
    const keyword = searchKeyword.value.toLowerCase()
    result = result.filter(t => 
      t.name.toLowerCase().includes(keyword) ||
      (t.description && t.description.toLowerCase().includes(keyword)) ||
      (t.useCases && t.useCases.toLowerCase().includes(keyword)) ||
      (t.tags && t.tags.some((tag: string) => tag.toLowerCase().includes(keyword)))
    )
  }
  
  return result
})

// 加载分类和模板
async function loadData() {
  try {
    // 加载分类
    await templateStore.fetchCategories()
    categories.value = templateStore.categories
    
    // 加载所有模板
    await templateStore.fetchTemplates()
    templates.value = templateStore.templates
  } catch (error: any) {
    console.error('加载模板失败:', error)
    message.error('加载模板失败')
  }
}

// 监听弹窗打开
watch(visible, (newVal) => {
  if (newVal) {
    loadData()
  }
})

// 选择模板
async function handleTemplateSelect(templateId: string) {
  try {
    workspaceStore.setGenerating(true)
    visible.value = false
    
    // 调用数据提取API，请求返回所有模板
    const generateModule = await import('@/api/generate')
    const response = await generateModule.generateAPI.extractData(
      workspaceStore.inputText,
      templateId,
      settingsStore.llmProvider,
      true // 请求返回所有模板
    )
    
    if (response.success && response.data) {
      const { config, selectedTemplate, allTemplates } = response.data
      
      // 更新配置并缓存
      workspaceStore.setSelectedTemplate(templateId)
      workspaceStore.setConfig(config)
      workspaceStore.cacheTemplateConfig(templateId, config)
      
      // 设置所有模板列表
      if (allTemplates && allTemplates.length > 0) {
        workspaceStore.setAllTemplates(allTemplates)
      }
      
      message.success(`已生成${selectedTemplate.templateName || selectedTemplate.templateId}`)
    } else {
      message.error('生成失败')
    }
  } catch (error: any) {
    console.error('生成失败:', error)
    message.error(error.message || '生成失败，请稍后重试')
  } finally {
    workspaceStore.setGenerating(false)
  }
}

function handleClose() {
  visible.value = false
}
</script>

<style scoped lang="scss">
.template-modal-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-height: 600px;
}

.search-bar {
  :deep(.ant-input-affix-wrapper) {
    border-radius: 8px;
  }
}

.category-tabs {
  :deep(.ant-radio-group) {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }
  
  :deep(.ant-radio-button-wrapper) {
    border-radius: 6px;
    border: 1px solid #d1d5db;
    
    &::before {
      display: none;
    }
    
    &:not(:first-child)::before {
      display: none;
    }
  }
}

.template-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 16px;
  max-height: 400px;
  overflow-y: auto;
  padding: 4px;
  
  &::-webkit-scrollbar {
    width: 8px;
  }
  
  &::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 4px;
  }
  
  &::-webkit-scrollbar-thumb {
    background: #c1c1c1;
    border-radius: 4px;
  }
  
  &::-webkit-scrollbar-thumb:hover {
    background: #a1a1a1;
  }
}

.template-item {
  cursor: pointer;
}

.template-card {
  position: relative;
  padding: 16px;
  background: #fff;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  transition: all 0.3s;
  min-height: 140px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  
  &:hover {
    border-color: #3b82f6;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
    transform: translateY(-2px);
  }
}

.category-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: 500;
  background: #e0e7ff;
  color: #4f46e5;
}

.template-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.template-name {
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
  padding-right: 60px;
}

.template-desc {
  font-size: 12px;
  color: #6b7280;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.template-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-top: auto;
}

.tag {
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 10px;
  background: #f3f4f6;
  color: #6b7280;
}

.empty-result {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 48px;
  color: #9ca3af;
  
  p {
    margin: 0;
    font-size: 14px;
  }
}
</style>
