<template>
  <div class="profile-page">
    <TopBar title="医生信息界面" />

    <div class="card">
      <h2>🧑‍⚕️ 基本信息</h2>

      <div class="info-row">
        <label>用户名：</label>
        <span>{{ userStore.username }}</span>
      </div>

      <div class="info-row">
        <label>角色：</label>
        <span>{{ userStore.role }}</span>
      </div>

      <div class="info-row bio-row">
        <label>简介：</label>
        <el-input
          type="textarea"
          v-model="biography"
          placeholder="请输入医生简介..."
          :rows="5"
        />
      </div>

      <el-button type="primary" @click="saveProfile">保存</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import TopBar from '@/components/TopBar.vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/userStore'

const userStore = useUserStore()
const biography = ref('')

// 加载简介信息
const loadProfile = async () => {
  try {
    const res = await axios.get('http://localhost:8000/doctor/profile/', {
      params: {
        user_id: localStorage.getItem('user_id'),
        role: localStorage.getItem('role')
      }
    })
    if (res.data.code === 200) {
      biography.value = res.data.data.biography
    } else {
      ElMessage.error(res.data.message || '加载失败')
    }
  } catch (err) {
    ElMessage.error('服务器连接失败')
  }
}

// 提交保存
const saveProfile = async () => {
  try {
    const res = await axios.post('http://localhost:8000/doctor/profile/update', {
      user_id: localStorage.getItem('user_id'),
      role: localStorage.getItem('role'),
      biography: biography.value
    })
    if (res.data.code === 200) {
      ElMessage.success('保存成功')
    } else {
      ElMessage.error(res.data.message || '保存失败')
    }
  } catch (err) {
    ElMessage.error('服务器连接失败')
  }
}

onMounted(loadProfile)
</script>

<style scoped>
.profile-page {
  padding: 120px 40px;
  background: #f6f8fb;
  min-height: 100vh;
}
.card {
  max-width: 600px;
  margin: auto;
  padding: 30px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}
.info-row {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 16px;
}
.bio-row label {
  align-self: flex-start;
}
</style>
