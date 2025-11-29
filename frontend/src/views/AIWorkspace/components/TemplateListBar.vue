<template>
  <div class="template-list-bar" v-if="allTemplates.length > 0" :class="{ 'collapsed': isCollapsed }">
    <div class="list-header">
      <div class="header-left">
        <span class="header-title">可选模板</span>
        <span class="header-count">{{ allTemplates.length }}个</span>
      </div>
      <button class="toggle-btn" @click="toggleCollapse" :title="isCollapsed ? '展开' : '折叠'">
        <ChevronLeft :size="16" :class="{ 'rotated': isCollapsed }" />
      </button>
    </div>
    
    <div class="template-scroll-container" v-if="!isCollapsed">
      <div class="template-cards">
        <div
          v-for="template in allTemplates"
          :key="template.templateId"
          class="template-card"
          :class="{ 'is-selected': template.templateId === selectedTemplateId }"
          @click="handleTemplateClick(template.templateId)"
        >
          <!-- 选中标识 -->
          <div v-if="template.templateId === selectedTemplateId" class="selected-badge">
            <Check :size="14" />
          </div>
          
          <!-- 相似度徽章 -->
          <div class="similarity-badge" :class="getSimilarityClass(template.similarityScore)">
            {{ Math.round(template.similarityScore * 100) }}%
          </div>
          
          <!-- 分类标签 -->
          <div class="category-tag">{{ getCategoryName(template.category) }}</div>
          
          <!-- 模板内容 -->
          <div class="template-content">
            <div class="template-name">{{ template.templateName }}</div>
            <div class="template-reason">{{ template.reason }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { Check, ChevronLeft } from 'lucide-vue-next'
import { message } from 'ant-design-vue'
import { useWorkspaceStore } from '@/stores/workspace'
import type { TemplateWithSimilarity } from '@/stores/workspace'

const workspaceStore = useWorkspaceStore()

const allTemplates = computed(() => workspaceStore.allTemplates)
const selectedTemplateId = computed(() => workspaceStore.selectedTemplateId)
const isCollapsed = ref(false)

function toggleCollapse() {
  isCollapsed.value = !isCollapsed.value
}

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

function getSimilarityClass(score: number): string {
  if (score >= 0.8) return 'high'
  if (score >= 0.6) return 'medium'
  if (score >= 0.4) return 'low'
  return 'very-low'
}

async function handleTemplateClick(templateId: string) {
  if (templateId === selectedTemplateId.value) {
    return // 已经是当前模板，不需要切换
  }
  
  try {
    // 检查缓存
    const cachedConfig = workspaceStore.getCachedConfig(templateId)
    if (cachedConfig) {
      console.log('[TemplateListBar] 使用缓存配置:', templateId)
      workspaceStore.setSelectedTemplate(templateId)
      workspaceStore.setConfig(cachedConfig)
      message.success('已切换模板')
      return
    }
    
    // 没有缓存，调用API生成
    workspaceStore.setGenerating(true)
    
    const generateModule = await import('@/api/generate')
    const response = await generateModule.generateAPI.extractData(
      workspaceStore.inputText,
      templateId,
      undefined,
      false // 不需要再次返回所有模板
    )
    
    if (response.success && response.data) {
      const { config } = response.data
      
      // 更新配置并缓存
      workspaceStore.setSelectedTemplate(templateId)
      workspaceStore.setConfig(config)
      workspaceStore.cacheTemplateConfig(templateId, config)
      
      message.success('已切换模板')
    } else {
      message.error('切换模板失败')
    }
  } catch (error: any) {
    console.error('切换模板失败:', error)
    message.error(error.message || '切换模板失败，请稍后重试')
  } finally {
    workspaceStore.setGenerating(false)
  }
}
</script>

<style scoped lang="scss">
.template-list-bar {
  width: 156px;
  height: 100%;
  background: #fff;
  border-right: 1px solid #f0f0f0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: width 0.3s ease;
  flex-shrink: 0;
  
  &.collapsed {
    width: 24px;
  }
}

.list-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 2px 4px;
  border-bottom: 1px solid #f0f0f0;
  background: #fafafa;
  flex-shrink: 0;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
  overflow: hidden;
  
  .collapsed & {
    display: none;
  }
}

.header-title {
  font-weight: 600;
  color: #1f2937;
  font-size: 12px;
  white-space: nowrap;
}

.header-count {
  font-size: 12px;
  color: #9ca3af;
  white-space: nowrap;
}

.toggle-btn {
  padding: 4px;
  background: transparent;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  transition: all 0.2s;
  flex-shrink: 0;
  
  &:hover {
    background: #f3f4f6;
    color: #3b82f6;
  }
  
  svg {
    transition: transform 0.3s ease;
    
    &.rotated {
      transform: rotate(180deg);
    }
  }
}

.template-scroll-container {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  
  &::-webkit-scrollbar {
    width: 6px;
  }
  
  &::-webkit-scrollbar-track {
    background: #f1f1f1;
  }
  
  &::-webkit-scrollbar-thumb {
    background: #c1c1c1;
    border-radius: 3px;
  }
  
  &::-webkit-scrollbar-thumb:hover {
    background: #a1a1a1;
  }
}

.template-cards {
  display: flex;
  flex-direction: column;
  gap: 3px;
  padding: 3px;
}

.template-card {
  position: relative;
  width: 100%;
  min-height: 65px;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 3px;
  padding: 3px;
  cursor: pointer;
  transition: all 0.3s;
  
  &:hover {
    transform: translateX(4px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    border-color: #3b82f6;
  }
  
  &.is-selected {
    border-color: #3b82f6;
    background: #eff6ff;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
}

.selected-badge {
  position: absolute;
  top: 8px;
  left: 8px;
  width: 24px;
  height: 24px;
  background: #3b82f6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  z-index: 2;
}

.similarity-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  color: white;
  
  &.high {
    background: #10b981;
  }
  
  &.medium {
    background: #3b82f6;
  }
  
  &.low {
    background: #f59e0b;
  }
  
  &.very-low {
    background: #9ca3af;
  }
}

.category-tag {
  position: absolute;
  top: 8px;
  left: 8px;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: 500;
  background: #e0e7ff;
  color: #4f46e5;
}

.template-card.is-selected .category-tag {
  left: 36px;
}

.template-content {
  margin-top: 32px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.template-name {
  font-size: 11px;
  font-weight: 600;
  color: #1f2937;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.template-reason {
  font-size: 10px;
  color: #6b7280;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: 1.3;
}
</style>
