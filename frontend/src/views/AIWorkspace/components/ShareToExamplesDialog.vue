<template>
  <div v-if="visible" class="share-dialog-overlay" @click.self="handleClose">
    <div class="share-dialog-modal">
      <!-- 头部 -->
      <div class="modal-header">
        <h3 class="modal-title">分享到示例库</h3>
        <button class="close-btn" @click="handleClose">
          <X :size="20" />
        </button>
      </div>
      
      <!-- 内容区 -->
      <div class="modal-body">
        <p class="description">
          您的作品将展示在示例页面,<br/>
          供其他用户参考学习。
        </p>
        
        <div class="form-group">
          <label class="form-label">作品标题（可选）</label>
          <input 
            v-model="title" 
            type="text" 
            class="form-input"
            :placeholder="defaultTitle"
            maxlength="50"
          />
          <span class="form-hint">留空则使用数据标题</span>
        </div>
      </div>
      
      <!-- 底部按钮 -->
      <div class="modal-footer">
        <button class="btn btn-secondary" @click="handleClose" :disabled="isSharing">
          取消
        </button>
        <button class="btn btn-primary" @click="handleConfirm" :disabled="isSharing">
          <Loader2 v-if="isSharing" :size="16" class="spinning" />
          <span>{{ isSharing ? '分享中...' : '确认分享' }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { X, Loader2 } from 'lucide-vue-next'
import { message } from 'ant-design-vue'
import { createWork } from '@/api/work'
import { useWorkspaceStore } from '@/stores/workspace'

interface Props {
  visible: boolean
  config: any
  inputText: string
}

const props = defineProps<Props>()
const emit = defineEmits<{
  (e: 'update:visible', value: boolean): void
  (e: 'success'): void
}>()

const workspaceStore = useWorkspaceStore()
const title = ref('')
const isSharing = ref(false)

// 默认标题（从配置中提取）
const defaultTitle = computed(() => {
  if (props.config?.data?.title) {
    return props.config.data.title
  }
  return '信息图作品'
})

// 关闭弹窗
const handleClose = () => {
  if (isSharing.value) return
  emit('update:visible', false)
}

// 确认分享
const handleConfirm = async () => {
  try {
    isSharing.value = true
    
    // 从 workspaceStore 获取模板ID，确保准确性
    const templateId = workspaceStore.selectedTemplateId
    
    if (!templateId) {
      message.error('未选择模板，无法分享')
      return
    }
    
    console.log('[ShareDialog] 分享作品:', {
      templateId,
      title: title.value.trim() || defaultTitle.value,
      inputText: props.inputText
    })
    
    // 准备作品数据
    const workData = {
      title: title.value.trim() || defaultTitle.value,
      templateId: templateId,
      inputText: props.inputText,
      infographicConfig: props.config
    }
    
    // 调用API保存作品
    const response = await createWork(workData)
    
    if (response.success) {
      message.success('分享成功！您的作品已添加到示例库')
      emit('success')
      emit('update:visible', false)
      
      // 重置标题
      title.value = ''
    } else {
      message.error('分享失败，请稍后重试')
    }
  } catch (error: any) {
    console.error('分享失败:', error)
    message.error(error.message || '分享失败，请稍后重试')
  } finally {
    isSharing.value = false
  }
}

// 监听visible变化，重置状态
watch(() => props.visible, (newVal) => {
  if (!newVal) {
    title.value = ''
    isSharing.value = false
  }
})

// 键盘ESC关闭
const handleKeyDown = (e: KeyboardEvent) => {
  if (e.key === 'Escape' && props.visible && !isSharing.value) {
    handleClose()
  }
}

watch(() => props.visible, (newVal) => {
  if (newVal) {
    document.addEventListener('keydown', handleKeyDown)
  } else {
    document.removeEventListener('keydown', handleKeyDown)
  }
})
</script>

<style scoped lang="scss">
.share-dialog-overlay {
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

.share-dialog-modal {
  background: white;
  border-radius: 8px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  max-width: 480px;
  width: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.close-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
  
  &:hover {
    background: #f3f4f6;
    color: #111827;
  }
}

.modal-body {
  padding: 1.5rem;
}

.description {
  color: #6b7280;
  font-size: 0.9375rem;
  line-height: 1.6;
  margin: 0 0 1.5rem 0;
  text-align: center;
}

.form-group {
  margin-bottom: 0;
}

.form-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
}

.form-input {
  width: 100%;
  padding: 0.625rem 0.875rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.9375rem;
  color: #111827;
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

.form-hint {
  display: block;
  font-size: 0.8125rem;
  color: #9ca3af;
  margin-top: 0.375rem;
}

.modal-footer {
  display: flex;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  border-top: 1px solid #e5e7eb;
  background: #f9fafb;
}

.btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  border: none;
  border-radius: 6px;
  font-size: 0.9375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
}

.btn-secondary {
  background: white;
  color: #374151;
  border: 1px solid #d1d5db;
  
  &:hover:not(:disabled) {
    background: #f9fafb;
    border-color: #9ca3af;
  }
}

.btn-primary {
  background: #3b82f6;
  color: white;
  
  &:hover:not(:disabled) {
    background: #2563eb;
  }
}

.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
