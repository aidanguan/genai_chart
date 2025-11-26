<template>
  <div class="workspace-hero">
    <div class="hero-content">
      <!-- 左侧标题和描述 -->
      <div class="hero-left">
        <h1 class="hero-title">
          <div class="title-icon">
            <span class="icon-text">图</span>
          </div>
          图表<span class="title-highlight">生成器</span>
        </h1>
        <p class="hero-description">
          将你在日常写作、汇报或其他文字工作中遇到的内容粘贴到这里，AI 会理解语境并为你生成相匹配的信息图方案
        </p>
      </div>
      
      <!-- 右侧装饰图标 -->
      <div class="hero-right">
        <div class="decoration-blur"></div>
        <Bot :size="50" class="bot-icon" />
        <div class="decoration-dot dot-1"></div>
        <div class="decoration-dot dot-2"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Bot } from 'lucide-vue-next'
</script>

<style scoped lang="scss">
.workspace-hero {
  width: 100%;
  flex-shrink: 0;
  padding: 0.5rem;
}

.hero-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.hero-left {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.hero-title {
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.title-icon {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  color: white;
  flex-shrink: 0;
}

.icon-text {
  font-size: 16px;
  font-weight: 700;
}

.title-highlight {
  color: #8b5cf6;
}

.hero-description {
  font-size: 12px;
  color: #6b7280;
  line-height: 1.5;
  max-width: 600px;
  margin: 0;
}

.hero-right {
  display: none;
  position: relative;
  width: 192px;
  height: 80px;
  align-items: center;
  justify-content: center;
}

.decoration-blur {
  position: absolute;
  inset: 0;
  background: #dbeafe;
  border-radius: 50%;
  filter: blur(48px);
  opacity: 0.4;
}

.bot-icon {
  position: relative;
  z-index: 10;
  color: #3b82f6;
  opacity: 0.8;
}

.decoration-dot {
  position: absolute;
  border-radius: 50%;
  animation: bounce 2s infinite;
  
  &.dot-1 {
    top: 0;
    right: 40px;
    width: 12px;
    height: 12px;
    background: #a78bfa;
    animation: bounce 2s infinite;
  }
  
  &.dot-2 {
    bottom: 16px;
    left: 40px;
    width: 8px;
    height: 8px;
    background: #06b6d4;
    animation: pulse 2s infinite;
  }
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-8px);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* 响应式 - 在较大屏幕显示装饰图标 */
@media (min-width: 768px) {
  .hero-right {
    display: flex;
  }
  
  .hero-title {
    font-size: 24px;
  }
  
  .title-icon {
    width: 40px;
    height: 40px;
  }
  
  .icon-text {
    font-size: 20px;
  }
  
  .hero-description {
    font-size: 13px;
  }
}

@media (max-width: 767px) {
  .workspace-hero {
    padding: 0.5rem;
  }
  
  .hero-title {
    font-size: 18px;
  }
  
  .title-icon {
    width: 28px;
    height: 28px;
  }
  
  .icon-text {
    font-size: 14px;
  }
}
</style>
