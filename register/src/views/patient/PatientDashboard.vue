<template>
  <div class="dashboard-wrapper">
    <TopBar title="用户挂号主页" />

    <div class="content">
      <div class="record-box">
        <h3>📋 您的挂号记录如下：</h3>

        <div v-if="records.length > 0" class="record-list">
          <div v-for="(record, index) in records" :key="index" class="record-item">
            <p>科室：{{ record.department }}</p>
            <p>医生：{{ record.doctor }}</p>
            <p>时间段：{{ record.timeSlot }}</p>
            <p>日期：{{ record.date }}</p>
          </div>
        </div>
        <div v-else class="no-records">
          暂无挂号记录，点击下方按钮立即挂号
        </div>
      </div>

      <!-- 去挂号按钮 -->
      <div class="btn-container">
        <button class="register-btn" @click="goRegister">去挂号</button>
      </div>
    </div>

    <!-- 悬浮“系统帮助”按钮 -->
    <button class="help-btn" @click="goHelp">❓系统帮助</button>
  </div>
</template>

<script setup>
import TopBar from '@/components/TopBar.vue'
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
import axios from 'axios'

const router = useRouter()
const records = ref([])

const goRegister = () => {
  router.push('/patient/register')
}

const goHelp = () => {
  router.push('/patient/help')
}

// ✅ 获取真实挂号记录（替换为后端接口）
onMounted(async () => {
  try {
    const userId = localStorage.getItem('user_id')
    const role = localStorage.getItem('role')
    const res = await axios.get('http://localhost:8000/patient/records/', {
                    params: {
                          user_id: userId,
                          role: role
                      }
})

    if (res.data.code === 200) {
      records.value = res.data.data || []
    }
  } catch (err) {
    console.error('获取挂号记录失败', err)
  }
})
</script>

<style scoped>
.dashboard-wrapper {
  font-family: Arial, sans-serif;
}

.content {
  padding: 40px;
  margin-top: 160px; /* 确保内容和顶栏分开 */
}

.record-box {
  border: 2px solid #0056ba;
  border-radius: 12px;
  padding: 24px;
  background-color: #f1f7ff;
  margin-bottom: 40px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  height: 500px;
  overflow-y: auto;
}

.record-box h3 {
  margin-bottom: 20px;
  font-size: 20px;
  color: #0056ba;
}

.record-list {
  margin-bottom: 20px;
}

.record-item {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 12px;
  background-color: #ffffff;
}

.no-records {
  color: #666;
  font-style: italic;
  padding: 12px;
}

.btn-container {
  display: flex;
  justify-content: center;
}

.register-btn {
  padding: 12px 24px;
  background-color: #007bff;
  border: none;
  color: white;
  font-size: 16px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s;
}
.register-btn:hover {
  background-color: #0056ba;
}

/* ✅ 悬浮帮助按钮 */
.help-btn {
  position: fixed;
  bottom: 24px;
  right: 24px;
  background-color: #6c757d;
  color: white;
  border: none;
  padding: 12px 18px;
  font-size: 14px;
  border-radius: 50px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
  cursor: pointer;
  z-index: 1000;
}
.help-btn:hover {
  background-color: #495057;
}
</style>
