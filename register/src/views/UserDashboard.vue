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
  </div>
</template>

<script setup>
import TopBar from '@/components/TopBar.vue'
import { useRouter } from 'vue-router'
import { ref } from 'vue'

const router = useRouter()

// 模拟挂号记录（后续可从后端获取）
const records = ref([
  {
    department: '内科',
    doctor: '张医生',
    timeSlot: '上午',
    date: '2025-04-18'
  },
  {
    department: '儿科',
    doctor: '李医生',
    timeSlot: '下午',
    date: '2025-04-19'
  }
])

const goRegister = () => {
  router.push('/register')
}
</script>

<style scoped>
.dashboard-wrapper {
  font-family: Arial, sans-serif;
}
.content {
  padding: 40px;
  margin-top: 160px; /* 确保内容和顶栏分开 */
}
/* ✅ 新增大卡片区域 */
.record-box {
  border: 2px solid #0056ba;
  border-radius: 12px;
  padding: 24px;
  background-color: #f1f7ff;
  margin-bottom: 40px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  height: 500px; /* 设置固定高度以启用滚动 */
  overflow-y: auto; /* 当内容超出时可滚动 */
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

/* ✅ 居中按钮容器 */
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
</style>
