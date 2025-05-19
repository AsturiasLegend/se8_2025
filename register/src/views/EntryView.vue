<template>
  <div class="entry-wrapper">
    <!-- ✅ 使用复用顶栏组件 -->
    <TopBar />

    <div class="main-content">
      <!-- 左侧登录入口 -->
      <div class="left-section">
        <!-- 第一行：图标 + 病人按钮 -->
        <div class="top-row">
            <button class="role-btn secondary" @click="goRegister">注册账号</button>
            <button class="role-btn primary" @click="goLogin">我是病人</button>
        </div>

        <!-- 第二行：医生 + 管理员 -->
        <div class="bottom-row">
            <button class="role-btn" @click="goDoctor">我是医生</button>
            <button class="role-btn" @click="goAdmin">我是管理员</button>
        </div>
    </div>

      <!-- 中线 -->
      <div class="divider"></div>

      <!-- 右侧宣传与帮助 -->
      <div class="right-section">
        <img class="banner" :src="hospitalImage" alt="宣传图" />
        <div class="buttons">
          <button class="info-btn">新闻动态</button>
          <button class="info-btn">国际交流</button>
          <button class="info-btn blue">使用帮助</button>
          <button class="info-btn">捐赠指南</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import TopBar from '@/components/TopBar.vue'  // ✅ 引入组件
import { useUserStore } from '@/stores/userStore'
import { useRouter } from 'vue-router'
import hospitalImage from '../assets/hospital-building.png'
import { onMounted } from 'vue'
const router = useRouter()
const userStore = useUserStore()

// ✅ 每次进入 Entry 页面自动清空登录状态
onMounted(() => {
    userStore.logout()
})
const goLogin = () => router.push('/login')
const goDoctor = () => router.push({ path: '/login', query: { role: 'doctor' } })
const goAdmin = () => router.push({ path: '/login', query: { role: 'administrator' } })
const goRegister = () => router.push('/register-user')
</script>

<style scoped>
.entry-wrapper {
  font-family: sans-serif;
}
.main-content {
  display: flex;
  height: calc(100vh - 200px); /* 扣除顶部栏高度 */
  align-items: center;        /* 垂直居中 */
  justify-content: space-around;
  padding: 20px;
}
.left-section, .right-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.left-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
}
 .top-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 280px; /* 与 .bottom-row 宽度一致 */
  gap: 30px;
}
.bottom-row {
  display: flex;
  gap: 20px;
  width: 280px;
  justify-content: space-between;
}

.symbol {
  width: 100px;
  margin-bottom: 10px;
}
.login-buttons {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.role-btn {
  width: 140px;
  height: 50px;
  font-size: 16px;
  border: 2px solid #0056ba;
  border-radius: 8px;
  background: white;
  cursor: pointer;
}
.role-btn.primary {
  width: 140px;
  height: 50px;
  font-size: 16px;
  border: 2px solid #0056ba;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  /* width: 130px;
  height: 50px;
  background: #0056ba;
  color: white; */
}
.role-btn.secondary {
  background: white;
  color: #0056ba;
  border: 2px solid #0056ba;
}
.divider {
  width: 2px;
  background: #ccc;
  margin: 0 30px;
}
.banner {
  width: 300px;
  border-radius: 8px;
  margin-bottom: 16px;
}
.buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}
.info-btn {
  width: 130px; 
  height: 50px;
  padding: 10px;
  font-size: 14px;
  border-radius: 6px;
  border: 2px solid #0056ba;
  background: white;
  cursor: pointer;
}
.info-btn.blue {
  background: #0056ba;
  color: white;
}
</style>
