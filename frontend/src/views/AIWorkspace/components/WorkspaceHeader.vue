<template>
  <header class="workspace-header">
    <div class="header-content">
      <!-- Logo 区域 -->
      <div class="header-left">
        <router-link to="/" class="logo-link">
          <div class="logo-icon">
            <Hexagon :size="20" fill="currentColor" />
          </div>
          <span class="logo-text">
            图表<span class="logo-highlight">生成器</span>
          </span>
        </router-link>
        
        <!-- 导航菜单 -->
        <nav class="nav-menu">
          <router-link to="/" class="nav-item" active-class="nav-item-active">
            首页
          </router-link>
          <router-link to="/examples" class="nav-item" active-class="nav-item-active">
            示例
          </router-link>
        </nav>
      </div>
      
      <!-- 用户信息区域 -->
      <div class="header-right">
        <!-- 用户菜单 -->
        <div class="user-menu" ref="menuRef">
          <button class="user-trigger" @click="toggleMenu">
            <div class="user-avatar">
              <User :size="16" />
            </div>
            <span class="user-name">用户</span>
            <ChevronDown :size="14" :class="['menu-arrow', { 'rotated': isMenuOpen }]" />
          </button>
          
          <!-- 下拉菜单 -->
          <div v-if="isMenuOpen" class="dropdown-menu">
            <div class="menu-section">
              <div class="menu-header">LLM配置</div>
              
              <button
                class="menu-item"
                :class="{ 'active': settingsStore.llmProvider === 'system' }"
                @click="handleProviderChange('system')"
              >
                <div class="menu-item-content">
                  <div class="menu-item-main">
                    <Cpu :size="16" />
                    <span class="menu-item-label">系统LLM</span>
                  </div>
                  <Check v-if="settingsStore.llmProvider === 'system'" :size="16" class="check-icon" />
                </div>
                <div class="menu-item-desc">使用内置AI模型</div>
              </button>
              
              <button
                class="menu-item"
                :class="{ 'active': settingsStore.llmProvider === 'dify' }"
                @click="handleProviderChange('dify')"
              >
                <div class="menu-item-content">
                  <div class="menu-item-main">
                    <Workflow :size="16" />
                    <span class="menu-item-label">Dify工作流</span>
                  </div>
                  <Check v-if="settingsStore.llmProvider === 'dify'" :size="16" class="check-icon" />
                </div>
                <div class="menu-item-desc">使用Dify平台处理</div>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { Hexagon, User, ChevronDown, Check, Cpu, Workflow } from 'lucide-vue-next'
import { useSettingsStore } from '@/stores/settings'

const settingsStore = useSettingsStore()
const isMenuOpen = ref(false)
const menuRef = ref<HTMLElement | null>(null)

function toggleMenu() {
  isMenuOpen.value = !isMenuOpen.value
}

function handleProviderChange(provider: 'system' | 'dify') {
  settingsStore.setLLMProvider(provider)
  isMenuOpen.value = false
}

// 点击外部关闭菜单
function handleClickOutside(event: MouseEvent) {
  if (menuRef.value && !menuRef.value.contains(event.target as Node)) {
    isMenuOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('mousedown', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('mousedown', handleClickOutside)
})
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
  gap: 2rem;
}

.logo-link {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: inherit;
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

.nav-menu {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.nav-item {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  text-decoration: none;
  color: #6b7280;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
  
  &:hover {
    color: #3b82f6;
    background: #f3f4f6;
  }
}

.nav-item-active {
  color: #3b82f6;
  background: #eff6ff;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-menu {
  position: relative;
}

.user-trigger {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background: transparent;
  border: 1px solid transparent;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  
  &:hover {
    background: #f9fafb;
    border-color: #e5e7eb;
  }
  
  &:focus {
    outline: none;
  }
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
  flex-shrink: 0;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: #6b7280;
}

.menu-arrow {
  color: #9ca3af;
  transition: transform 0.2s;
  flex-shrink: 0;
  
  &.rotated {
    transform: rotate(180deg);
  }
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 260px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e7eb;
  overflow: hidden;
  z-index: 100;
  animation: fadeIn 0.15s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(-8px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.menu-section {
  padding: 8px;
}

.menu-header {
  padding: 8px 12px;
  font-size: 12px;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.menu-item {
  width: 100%;
  text-align: left;
  padding: 10px 12px;
  background: transparent;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.15s;
  margin-bottom: 4px;
  
  &:hover {
    background: #f9fafb;
  }
  
  &.active {
    background: #eff6ff;
    
    .menu-item-label {
      color: #3b82f6;
      font-weight: 600;
    }
  }
  
  &:last-child {
    margin-bottom: 0;
  }
}

.menu-item-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 4px;
}

.menu-item-main {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #374151;
}

.menu-item-label {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.menu-item-desc {
  font-size: 12px;
  color: #9ca3af;
  padding-left: 26px;
}

.check-icon {
  color: #3b82f6;
  flex-shrink: 0;
}
</style>
