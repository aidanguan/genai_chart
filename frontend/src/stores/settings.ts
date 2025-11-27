/**
 * 用户设置状态管理
 * 管理LLM提供商选择等全局配置
 */
import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export type LLMProvider = 'system' | 'dify'

const STORAGE_KEY = 'user_settings'

interface UserSettings {
  llmProvider: LLMProvider
}

// 从localStorage加载设置
function loadSettings(): UserSettings {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (stored) {
      const parsed = JSON.parse(stored)
      return {
        llmProvider: parsed.llmProvider || 'system'
      }
    }
  } catch (error) {
    console.warn('Failed to load settings from localStorage:', error)
  }
  return {
    llmProvider: 'system' // 默认使用系统LLM
  }
}

// 保存设置到localStorage
function saveSettings(settings: UserSettings) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(settings))
  } catch (error) {
    console.warn('Failed to save settings to localStorage:', error)
  }
}

export const useSettingsStore = defineStore('settings', () => {
  // 加载初始设置
  const initialSettings = loadSettings()
  
  // 状态
  const llmProvider = ref<LLMProvider>(initialSettings.llmProvider)
  
  // 监听变化并自动保存
  watch(
    () => llmProvider.value,
    () => {
      saveSettings({
        llmProvider: llmProvider.value
      })
    }
  )
  
  // 操作
  function setLLMProvider(provider: LLMProvider) {
    llmProvider.value = provider
  }
  
  function toggleLLMProvider() {
    llmProvider.value = llmProvider.value === 'system' ? 'dify' : 'system'
  }
  
  return {
    // 状态
    llmProvider,
    // 操作
    setLLMProvider,
    toggleLLMProvider
  }
})
