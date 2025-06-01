<template>
  <div class="dashboard-wrapper">
    <TopBar title="医生功能菜单" />

    <div class="main">
      <h2 class="welcome">欢迎使用 XXX 医院线上挂号系统</h2>
      <div class="card-container">
        <div class="card" @click="goTo('/doctor/profile')">
          🧑‍⚕️ 基本信息
        </div>
        <div class="card" @click="goTo('/doctor/appointmentsetting')">
          📅 号源管理
        </div>
        <div class="card" @click="goTo('/doctor/diagnosislist')">
          📋 接诊管理
        </div>
        <div class="card" @click="goTo('/doctor/help')">
          💡 系统帮助
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import TopBar from '@/components/TopBar.vue'
import { useRouter } from 'vue-router'
const router = useRouter()

const goTo = (path) => {
  router.push(path)
}
</script>

<style scoped>
.dashboard-wrapper {
  font-family: sans-serif;
}

.main {
  padding-top: 200px;
  text-align: center;
}

.welcome {
  font-size: 24px;
  margin-bottom: 40px;
}

.card-container {
  display: flex;
  justify-content: center;
  gap: 40px;
  flex-wrap: wrap;
}

.card {
  width: 160px;
  height: 120px;
  background: #ffffff;
  border: 2px solid #0056ba;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  font-size: 18px;
  color: #0056ba;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: 0.3s;
}

.card:hover {
  background-color: #0056ba;
  color: white;
}
</style>
