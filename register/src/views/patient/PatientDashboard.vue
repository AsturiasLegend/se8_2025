<template>
  <div class="dashboard-wrapper">
    <TopBar title="用户挂号主页" />

    <div class="btn-container">
      <button class="register-btn" @click="goRegister">去挂号</button>
    </div>


    <div class="content">
      <div class="record-box">
        <h3>📋 您的挂号记录如下：</h3>

        <div v-if="records.length > 0" class="record-list">
          <div v-for="(record, index) in records" :key="index" class="record-item">
            <p>医生：{{ record.doctor_name }}</p>
            <p>科室：{{ record.department}}</p>
            <p>时间：{{ record.appointment_time }} - {{ record.appointment_end_time }}</p>
            <p>状态：{{ record.status_display }}</p>
            <p>挂号时间：{{ record.timestamp }}</p>

            <button v-if="record.can_cancel" class="cancel-btn" @click="cancelRecord(record.order_id)">取消挂号</button>
          </div>
        </div>
        <div v-else class="no-records">
          暂无挂号记录，点击下方按钮立即挂号
        </div>
      </div>

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
import { ElMessage } from 'element-plus'

const router = useRouter()
const records = ref([])

const fetchRecords = async () => {
  try {
    const userId = localStorage.getItem('user_id')
    const role = localStorage.getItem('role')
    const res = await axios.get('http://localhost:8000/patient/records/', {
      params: { user_id: userId, role }
    })

    if (res.data.code === 200) {
      records.value = res.data.data || []
    }
  } catch (err) {
    console.error('获取挂号记录失败', err)
  }
}

const cancelRecord = async (orderId) => {
  try {
    const res = await axios.post('http://localhost:8000/patient/cancel/', {
      user_id: localStorage.getItem('user_id'),
      role: localStorage.getItem('role'),
      order_id: orderId
    })

    if (res.data.code === 200) {
      ElMessage.success('挂号取消成功')
      await fetchRecords()
    } else {
      ElMessage.error(res.data.message || '取消失败')
    }
  } catch (err) {
    ElMessage.error('服务器连接失败')
  }
}

const goRegister = () => {
  router.push('/patient/register')
}

const goHelp = () => {
  router.push('/patient/help')
}

onMounted(fetchRecords)
</script>

<style scoped>
.dashboard-wrapper {
  font-family: Arial, sans-serif;
}

.content {
  padding: 40px;
  margin-top: 160px;
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

.record-item {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 12px;
  background-color: #ffffff;
}

.cancel-btn {
  margin-top: 10px;
  padding: 8px 16px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.cancel-btn:hover {
  background-color: #c82333;
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
