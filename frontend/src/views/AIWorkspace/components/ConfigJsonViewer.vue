<template>
  <div v-if="visible" class="config-json-viewer-overlay" @click.self="handleClose">
    <div class="config-json-viewer-modal">
      <!-- 头部 -->
      <div class="modal-header">
        <h3 class="modal-title">信息图配置代码</h3>
        <div class="header-actions">
          <button class="header-btn" @click="handleCopy" :disabled="copied">
            <Check v-if="copied" :size="16" />
            <Copy v-else :size="16" />
            <span>{{ copied ? '已复制' : '复制' }}</span>
          </button>
          <button class="header-btn close-btn" @click="handleClose">
            <X :size="16" />
            <span>关闭</span>
          </button>
        </div>
      </div>
      
      <!-- JSON代码区域 -->
      <div class="modal-body">
        <pre class="json-code"><code>{{ formattedJson }}</code></pre>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { Copy, Check, X } from 'lucide-vue-next'
import { message } from 'ant-design-vue'

interface Props {
  visible: boolean
  config: any
}

const props = defineProps<Props>()
const emit = defineEmits<{
  (e: 'update:visible', value: boolean): void
}>()

const copied = ref(false)

// 格式化JSON配置
const formattedJson = computed(() => {
  if (!props.config) return '{}'
  try {
    return JSON.stringify(props.config, null, 2)
  } catch (error) {
    console.error('JSON格式化失败:', error)
    return '{}'
  }
})

// 复制到剪贴板
const handleCopy = async () => {
  try {
    await navigator.clipboard.writeText(formattedJson.value)
    copied.value = true
    message.success('配置已复制到剪贴板')
    
    // 2秒后重置复制状态
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (error) {
    console.error('复制失败:', error)
    message.error('复制失败，请手动复制')
  }
}

// 关闭弹窗
const handleClose = () => {
  emit('update:visible', false)
}

// 监听visible变化，重置复制状态
watch(() => props.visible, (newVal) => {
  if (!newVal) {
    copied.value = false
  }
})

// 键盘ESC关闭
const handleKeyDown = (e: KeyboardEvent) => {
  if (e.key === 'Escape' && props.visible) {
    handleClose()
  }
}

// 添加和移除键盘监听
watch(() => props.visible, (newVal) => {
  if (newVal) {
    document.addEventListener('keydown', handleKeyDown)
  } else {
    document.removeEventListener('keydown', handleKeyDown)
  }
})
</script>

<style scoped lang="scss">
.config-json-viewer-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 2rem;
}

.config-json-viewer-modal {
  background: white;
  border-radius: 8px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  max-width: 800px;
  width: 100%;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 0.5rem;
}

.header-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: white;
  color: #374151;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
  
  &:hover:not(:disabled) {
    background: #f9fafb;
    border-color: #9ca3af;
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
}

.close-btn {
  color: #6b7280;
  
  &:hover {
    color: #111827;
    background: #f3f4f6;
  }
}

.modal-body {
  flex: 1;
  overflow: auto;
  padding: 0;
  background: #1f2937;
}

.json-code {
  margin: 0;
  padding: 1.5rem;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', 'Consolas', 'source-code-pro', monospace;
  font-size: 0.875rem;
  line-height: 1.6;
  color: #e5e7eb;
  background: #1f2937;
  overflow-x: auto;
  white-space: pre;
  
  code {
    font-family: inherit;
  }
}

/* 滚动条样式 */
.modal-body::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.modal-body::-webkit-scrollbar-track {
  background: #374151;
}

.modal-body::-webkit-scrollbar-thumb {
  background: #6b7280;
  border-radius: 4px;
  
  &:hover {
    background: #9ca3af;
  }
}
</style>
