<template>
  <div class="ai-workspace">
    <!-- 左侧输入区 -->
    <div class="input-panel">
      <LeftInputPanel />
    </div>
    
    <!-- 右侧预览区 -->
    <div class="preview-panel">
      <RightPreviewPanel />
    </div>
  </div>
</template>

<script setup lang="ts">
import LeftInputPanel from './components/LeftInputPanel.vue'
import RightPreviewPanel from './components/RightPreviewPanel.vue'
import { onMounted } from 'vue'
import { useTemplateStore } from '@/stores/template'

const templateStore = useTemplateStore()

onMounted(() => {
  // 初始化时加载分类数据
  templateStore.fetchCategories()
})
</script>

<style scoped lang="scss">
.ai-workspace {
  height: 100%;
  display: flex;
  background: #f5f5f5;
  overflow: hidden;
}

.input-panel {
  width: 480px;
  min-width: 400px;
  max-width: 600px;
  background: #fff;
  border-right: 1px solid #d9d9d9;
  overflow: hidden;
  min-height: 0;
  flex-shrink: 0;
}

.preview-panel {
  flex: 1;
  background: #fafafa;
  overflow: hidden;
  min-height: 0;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .workspace-content {
    flex-direction: column;
  }
  
  .input-panel {
    width: 100%;
    height: 40%;
    border-right: none;
    border-bottom: 1px solid #d9d9d9;
  }
  
  .preview-panel {
    height: 60%;
  }
}
</style>
