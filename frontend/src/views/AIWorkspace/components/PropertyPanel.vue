<template>
  <div class="property-panel" v-if="visible">
    <!-- 面板头部 -->
    <div class="panel-header">
      <h3 class="panel-title">属性编辑器</h3>
      <button class="close-btn" @click="handleClose" title="关闭">
        <X :size="18" />
      </button>
    </div>
    
    <!-- 选中元素信息 -->
    <div class="panel-section" v-if="selectedElement">
      <div class="section-header">
        <span class="section-title">选中</span>
      </div>
      <div class="element-info">
        <span class="element-type">{{ getElementTypeName(selectedElement.type) }}</span>
      </div>
    </div>
    
    <!-- 文本编辑区域 -->
    <div class="panel-section" v-if="selectedElement">
      <div class="section-header">
        <span class="section-title">文本</span>
      </div>
      <div class="input-group">
        <textarea 
          v-model="editValue"
          class="text-input"
          rows="3"
          @input="handleTextChange"
          placeholder="输入文本内容"
        />
      </div>
    </div>
    
    <!-- 可见性控制 -->
    <div class="panel-section" v-if="selectedElement">
      <div class="section-header">
        <span class="section-title">可见性</span>
      </div>
      <div class="visibility-control">
        <label class="checkbox-label">
          <input 
            type="checkbox" 
            v-model="elementVisible"
            @change="handleVisibilityChange"
          />
          <span>显示</span>
        </label>
      </div>
    </div>
    
    <!-- 配色方案（全局） -->
    <div class="panel-section">
      <div class="section-header">
        <span class="section-title">配色</span>
        <span class="section-badge">全局</span>
      </div>
      <div class="color-controls">
        <div class="color-item">
          <label class="color-label">主色</label>
          <div class="color-picker-wrapper">
            <input 
              type="color" 
              v-model="primaryColor"
              @change="handlePrimaryColorChange"
              class="color-input"
            />
            <span class="color-value">{{ primaryColor }}</span>
          </div>
          <div class="color-hint" v-if="selectedPalette">
            💡 修改主色会自动清空调色板
          </div>
        </div>
        <div class="color-item">
          <label class="color-label">背景</label>
          <div class="color-picker-wrapper">
            <input 
              type="color" 
              v-model="bgColor"
              @change="handleBgColorChange"
              class="color-input"
            />
            <span class="color-value">{{ bgColor }}</span>
          </div>
        </div>
        <div class="color-item">
          <label class="color-label">调色板</label>
          <select class="palette-select" v-model="selectedPalette" @change="handlePaletteChange">
            <option value="">默认（使用主色）</option>
            <option value="antv">AntV默认</option>
            <option value="business">商务蓝</option>
            <option value="vibrant">活力渐变</option>
            <option value="fresh">清新绿</option>
            <option value="purple">紫色系</option>
          </select>
          <div class="color-hint">
            💡 选择调色板会覆盖主色
          </div>
        </div>
      </div>
    </div>
    
    <!-- 空状态 -->
    <div class="empty-state" v-if="!selectedElement">
      <div class="empty-icon">
        <MousePointerClick :size="32" />
      </div>
      <p class="empty-text">点击画布中的元素<br/>进行编辑</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { X, MousePointerClick } from 'lucide-vue-next'

interface ElementSelection {
  type: 'title' | 'desc' | 'item' | 'item-field'
  path: string
  value: any
}

interface Props {
  visible?: boolean
  selectedElement?: ElementSelection | null
  config?: any
}

interface Emits {
  (e: 'update:visible', value: boolean): void
  (e: 'text-change', data: { path: string; value: string }): void
  (e: 'visibility-change', data: { path: string; visible: boolean }): void
  (e: 'color-change', data: { type: 'primary' | 'bg' | 'palette'; value: any }): void
}

const props = withDefaults(defineProps<Props>(), {
  visible: false,
  selectedElement: null,
  config: null
})

const emit = defineEmits<Emits>()

// 本地状态
const editValue = ref('')
const elementVisible = ref(true)
const primaryColor = ref('#FF356A')
const bgColor = ref('#FFFFFF')
const selectedPalette = ref('')

// 计算属性 - 属性面板可见性
const isPanelVisible = computed(() => props.visible)

// 监听选中元素变化
watch(() => props.selectedElement, (newElement) => {
  if (newElement) {
    editValue.value = newElement.value || ''
    elementVisible.value = true
  } else {
    editValue.value = ''
  }
}, { immediate: true })

// 监听配置变化
watch(() => props.config, (newConfig) => {
  if (newConfig && newConfig.themeConfig) {
    primaryColor.value = newConfig.themeConfig.colorPrimary || '#FF356A'
    bgColor.value = newConfig.themeConfig.colorBg || '#FFFFFF'
  }
}, { deep: true, immediate: true })

// 方法
function handleClose() {
  emit('update:visible', false)
}

function getElementTypeName(type: string): string {
  const typeMap: Record<string, string> = {
    'title': '标题文本',
    'desc': '描述文本',
    'item': '数据项',
    'item-field': '数据字段'
  }
  return typeMap[type] || type
}

function handleTextChange() {
  if (props.selectedElement) {
    emit('text-change', {
      path: props.selectedElement.path,
      value: editValue.value
    })
  }
}

function handleVisibilityChange() {
  if (props.selectedElement) {
    emit('visibility-change', {
      path: props.selectedElement.path,
      visible: elementVisible.value
    })
  }
}

function handlePrimaryColorChange() {
  // 修改主色时，同步更新调色板，确保主色生效
  // 优先级：palette > colorPrimary，所以需要同时更新palette
  emit('color-change', {
    type: 'primary',
    value: primaryColor.value
  })
  
  // 清空调色板选择，让主色生效
  selectedPalette.value = ''
}

function handleBgColorChange() {
  emit('color-change', {
    type: 'bg',
    value: bgColor.value
  })
}

function handlePaletteChange() {
  const palettes: Record<string, string[]> = {
    'antv': ['#5B8FF9', '#5AD8A6', '#5D7092', '#F6BD16', '#E86452'],
    'business': ['#1890ff', '#096dd9', '#0050b3', '#003a8c', '#002766'],
    'vibrant': ['#f94144', '#f3722c', '#f8961e', '#f9c74f', '#90be6d'],
    'fresh': ['#52c41a', '#73d13d', '#95de64', '#b7eb8f', '#d9f7be'],
    'purple': ['#722ed1', '#9254de', '#b37feb', '#d3adf7', '#efdbff']
  }
  
  // 如果选择了"默认"，清空调色板，让主色生效
  if (!selectedPalette.value || selectedPalette.value === '') {
    emit('color-change', {
      type: 'palette',
      value: null  // 清空调色板
    })
    return
  }
  
  const palette = palettes[selectedPalette.value]
  if (palette) {
    emit('color-change', {
      type: 'palette',
      value: palette
    })
  }
}
</script>

<style scoped lang="scss">
.property-panel {
  width: 300px;
  height: 100%;
  background: #fff;
  border-left: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.panel-header {
  padding: 16px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.panel-title {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.close-btn {
  padding: 4px;
  background: transparent;
  border: none;
  color: #6b7280;
  cursor: pointer;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  
  &:hover {
    background: #f3f4f6;
  }
}

.panel-section {
  padding: 16px;
  border-bottom: 1px solid #f3f4f6;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.section-title {
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.section-badge {
  font-size: 11px;
  padding: 2px 8px;
  background: #eff6ff;
  color: #3b82f6;
  border-radius: 4px;
  font-weight: 500;
}

.element-info {
  padding: 8px 12px;
  background: #f9fafb;
  border-radius: 6px;
}

.element-type {
  font-size: 13px;
  color: #6b7280;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.text-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 13px;
  color: #1f2937;
  resize: vertical;
  transition: all 0.2s;
  
  &:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
  
  &::placeholder {
    color: #9ca3af;
  }
}

.visibility-control {
  display: flex;
  align-items: center;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 13px;
  color: #374151;
  
  input[type="checkbox"] {
    width: 16px;
    height: 16px;
    cursor: pointer;
  }
}

.color-controls {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.color-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.color-label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
}

.color-picker-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
}

.color-input {
  width: 40px;
  height: 32px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  cursor: pointer;
  
  &::-webkit-color-swatch-wrapper {
    padding: 2px;
  }
  
  &::-webkit-color-swatch {
    border: none;
    border-radius: 4px;
  }
}

.color-value {
  font-size: 12px;
  color: #6b7280;
  font-family: monospace;
}

.palette-select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 13px;
  color: #1f2937;
  background: #fff;
  cursor: pointer;
  transition: all 0.2s;
  
  &:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
}

.color-hint {
  margin-top: 4px;
  font-size: 11px;
  color: #9ca3af;
  line-height: 1.4;
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 32px;
  text-align: center;
}

.empty-icon {
  margin-bottom: 16px;
  color: #d1d5db;
}

.empty-text {
  font-size: 13px;
  color: #9ca3af;
  line-height: 1.5;
  margin: 0;
}
</style>
