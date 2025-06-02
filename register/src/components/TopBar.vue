<template>
  <header class="top-bar">
    <div class="logo">
      🏥 XXX医院线上挂号系统
    </div>
    <div class="user-section" v-if="userStore.role">
      <button class="info-btn" @click="goProfile">基本信息</button>
      <span class="user-info">👤 {{ userStore.username }}</span>
      <button class="logout-btn" @click="logout">退出</button>
    </div>
  </header>
</template>

<script setup>
import { useUserStore } from '@/stores/userStore'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const router = useRouter()

const logout = () => {
  userStore.logout()
  ElMessage.success('退出成功')
  router.push('/entry')
}

const goProfile = () => {
  if (userStore.role === 'doctor') {
    router.push('/doctor/profile')
  } else if (userStore.role === 'patient') {
    router.push('/patient/profile')
  }
}
</script>

<style scoped>
.top-bar {
  height: 100px;
  background-color: #0056ba;
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  font-size: 40px;
  font-weight: bold;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 999;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-section {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 18px;
}

.info-btn {
  background: white;
  color: #0056ba;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
}
.info-btn:hover {
  background: #f5f5f5;
}

.logout-btn {
  background: white;
  color: #0056ba;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
}
.logout-btn:hover {
  background: #f5f5f5;
}
</style>
