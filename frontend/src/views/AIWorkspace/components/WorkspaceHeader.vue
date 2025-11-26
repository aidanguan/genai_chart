<template>
  <header class="workspace-header">
    <div class="header-content">
      <!-- Logo 区域 -->
      <div class="header-left">
        <div class="logo-icon">
          <Hexagon :size="20" fill="currentColor" />
        </div>
        <span class="logo-text">
          图表<span class="logo-highlight">生成器</span>
        </span>
      </div>
      
      <!-- 用户信息区域 -->
      <div class="header-right">
        <div class="user-avatar">
          <User :size="16" />
        </div>
        <span class="user-name">用户</span>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { Hexagon, User } from 'lucide-vue-next'
</script>

<style scoped lang="scss">
.workspace-header {
  width: 100%;
  background: #fff;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  border-bottom: 1px solid #f0f0f0;
  flex-shrink: 0;
  position: sticky;
  top: 0;
  z-index: 50;
  margin: 0;
  padding: 0;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 24px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo-icon {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.025em;
  color: #1f2937;
}

.logo-highlight {
  color: #8b5cf6;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #fb923c 0%, #fbbf24 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  border: 1px solid #e5e7eb;
  color: white;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: #6b7280;
}
</style>
