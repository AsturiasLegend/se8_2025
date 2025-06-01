<template>
  <div class="profile-wrapper">
    <TopBar title="患者基本信息" />

    <div class="profile-card">
      <h2>🧾 患者信息</h2>
      <div v-if="info">
        <p><strong>姓名：</strong>{{ info.real_name }}</p>
        <p><strong>身份证号：</strong>{{ info.id_card }}</p>
        <p><strong>手机号：</strong>{{ info.phone }}</p>
        <p><strong>账号：</strong>{{ info.username }}</p>
      </div>
      <div v-else>
        <p>正在加载信息...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import TopBar from '@/components/TopBar.vue'
import { onMounted, ref } from 'vue'
import axios from 'axios'

const info = ref(null)

onMounted(async () => {
  const userId = localStorage.getItem('user_id')
  const role = localStorage.getItem('role')

  try {
    const res = await axios.get('http://localhost:8000/patient/profile/', {
      params: {
        user_id: userId,
        role: role
      }
    })
    if (res.data.code === 200) {
      info.value = res.data.data
    } else {
      console.error(res.data.message)
    }
  } catch (err) {
    console.error('获取信息失败：', err)
  }
})
</script>

<style scoped>
.profile-wrapper {
  padding-top: 120px;
  background: #eef3f5;
  min-height: 100vh;
}

.profile-card {
  max-width: 600px;
  margin: 40px auto;
  padding: 30px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
  font-size: 16px;
}

.profile-card h2 {
  margin-bottom: 20px;
  color: #0056ba;
}

.profile-card p {
  margin-bottom: 12px;
  line-height: 1.6;
}
</style>
