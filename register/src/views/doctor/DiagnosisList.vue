<template>
  <div class="diagnosis-list">
    <TopBar title="接诊管理" />
    <h2>🩺 接诊队列</h2>

    <el-table :data="orders" border style="width: 100%">
      <el-table-column prop="time" label="挂号时间" min-width="25%" />
      <el-table-column prop="patient_name" label="患者姓名" min-width="25%" />
      <el-table-column prop="status" label="状态" min-width="20%" />
      <el-table-column label="操作" min-width="30%">
        <template #default="{ row }">
          <el-button v-if="row.status === 'pending'" size="small" type="primary" @click="handleStatus(row, 'diagnosing')">提前接诊</el-button>
          <el-button v-if="row.status === 'diagnosing'" size="small" type="success" @click="handleStatus(row, 'completed')">完成接诊</el-button>
          <el-button size="small" type="danger" @click="reportException(row)">报告异常</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import TopBar from '@/components/TopBar.vue'

const orders = ref([])

const fetchOrders = async () => {
  try {
    const userId = localStorage.getItem('user_id')
    const role = localStorage.getItem('role')
    const res = await axios.get('http://localhost:8000/doctor/dashboard/', {
                      params: {
                        user_id: userId,
                        role: role
                      }
    })
    if (res.data.code === 200) {
      orders.value = res.data.data
    } else {
      ElMessage.error(res.data.message || '加载失败')
    }
  } catch {
    ElMessage.error('无法连接服务器')
  }
}

const handleStatus = async (row, status) => {
  try {
    const userId = localStorage.getItem('user_id')
    const role = localStorage.getItem('role')
    const res = await axios.post('http://localhost:8000/doctor/dashboard/', {
      user_id: userId,
      role: role,
      order_id: row.order_id,
      status
    })
    if (res.data.code === 200) {
      ElMessage.success('状态更新成功')
      fetchOrders()
    } else {
      ElMessage.error(res.data.message || '更新失败')
    }
  } catch {
    ElMessage.error('服务器连接失败')
  }
}

const reportException = (row) => {
  // 跳转异常上报页
  window.location.href = `/doctor/exceptionreport?order_id=${row.order_id}`
}

onMounted(fetchOrders)
</script>

<style scoped>
.diagnosis-list {
  padding: 160px 40px;
}
h2 {
  margin-bottom: 16px;
}
</style>
