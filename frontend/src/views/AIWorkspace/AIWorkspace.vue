<template>
  <div class="ai-workspace">
    <!-- Header 顶部导航 -->
    <WorkspaceHeader />
    
    <!-- Main Content 主要内容区域 -->
    <main class="workspace-main">
      <!-- Workspace Grid 工作区网格 -->
      <div class="workspace-grid">
        <!-- 左侧输入区 -->
        <div class="input-section">
          <LeftInputPanel />
        </div>
        
        <!-- 右侧预览区 -->
        <div class="preview-section">
          <RightPreviewPanel />
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import WorkspaceHeader from './components/WorkspaceHeader.vue'
import LeftInputPanel from './components/LeftInputPanel.vue'
import RightPreviewPanel from './components/RightPreviewPanel.vue'
import { useTemplateStore } from '@/stores/template'

const templateStore = useTemplateStore()

onMounted(() => {
  // 初始化时加载分类数据
  templateStore.fetchCategories()
})
</script>

<style scoped lang="scss">
.ai-workspace {
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  margin: 0;
  padding: 0;
}

.workspace-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  width: 100%;
  margin: 0;
  padding: 0;
  gap: 0;
}

@media (min-width: 768px) {
  .workspace-main {
    padding: 0;
    gap: 0;
  }
}

.workspace-grid {
  min-height: 0;
  display: flex;
  gap: 1.5rem;
  height: 98%;      // 上下各留1%的边距
  width: 90%;       // 使用浏览器的90%宽度
  margin: 1% auto;  // 上下1%边距，左右居中
  padding: 0 1.5rem;
}

.input-section {
  min-height: 0;
  height: 100%;
  width: 21%;      // 输入区占工作区的21%（从30%减少30%）
  min-width: 360px; // 设置最小宽度，避免过小
  max-width: 600px; // 设置最大宽度，避免过大
  flex-shrink: 0;
}

.preview-section {
  min-height: 0;
  height: 100%;
  flex: 1;
  min-width: 0;
}

/* 响应式设计 */
@media (max-width: 1023px) {
  .workspace-grid {
    grid-template-columns: 1fr;
    grid-template-rows: 40% 60%;
  }
}


</style>
