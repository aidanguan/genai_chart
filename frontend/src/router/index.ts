/**
 * 路由配置
 */
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'workspace',
      component: () => import('@/views/AIWorkspace/AIWorkspace.vue')
    }
  ]
})

// 添加错误处理
router.onError((error) => {
  console.error('路由错误:', error)
  console.error('错误详情:', {
    message: error.message,
    stack: error.stack,
    name: error.name,
    cause: error.cause
  })
})

export default router
