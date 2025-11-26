<template>
  <div class="ai-workspace">
    <!-- Header 顶部导航 -->
    <WorkspaceHeader />
    
    <!-- Main Content 主要内容区域 -->
    <main class="workspace-main">
      <!-- Hero 简介区域 -->
      <div class="workspace-hero">
        <WorkspaceHero />
      </div>
      
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
import WorkspaceHero from './components/WorkspaceHero.vue'
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
  max-width: 1600px;
  margin: 0 auto;
  padding: 0.75rem;
  gap: 0.75rem;
}

@media (min-width: 768px) {
  .workspace-main {
    padding: 1rem;
    gap: 1rem;
  }
}

.workspace-hero {
  flex-shrink: 0;
}

.workspace-grid {
  flex: 1;
  min-height: 0;
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.75rem;
  height: 100%;
}

@media (min-width: 1024px) {
  .workspace-grid {
    grid-template-columns: repeat(12, 1fr);
    gap: 0.75rem;
  }
  
  .input-section {
    grid-column: span 4;
  }
  
  .preview-section {
    grid-column: span 8;
  }
}

@media (min-width: 1280px) {
  .workspace-grid {
    gap: 1rem;
  }
  
  .input-section {
    grid-column: span 3;
  }
  
  .preview-section {
    grid-column: span 9;
  }
}

.input-section {
  min-height: 0;
  height: 100%;
}

.preview-section {
  min-height: 0;
  height: 100%;
}

/* 响应式设计 */
@media (max-width: 1023px) {
  .workspace-grid {
    grid-template-columns: 1fr;
    grid-template-rows: 40% 60%;
  }
}


</style>
