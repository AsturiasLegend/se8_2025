<template>
  <div class="setting-page">
    <TopBar title="号源设置" />

    <div class="card">
      <h2>📅 设置号源</h2>

      <div class="form-group">
        <label>医生姓名：{{ userStore.username }}</label>
        <label>科室：自动获取（可省略）</label>

        <label>选择日期：</label>
        <el-date-picker
          v-model="date"
          type="date"
          placeholder="选择日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
        />

        <label>添加时间段（起止时间）：</label>
        <div v-for="(slot, index) in timeSlots" :key="index" class="slot-row">
          <el-time-picker
            v-model="slot.start"
            placeholder="开始时间"
            format="HH:mm"
            value-format="HH:mm"
          />
          <el-time-picker
            v-model="slot.end"
            placeholder="结束时间"
            format="HH:mm"
            value-format="HH:mm"
          />
          <input
            type="number"
            v-model="slot.quota"
            placeholder="最大号源量"
            min="1"
          />
          <el-button type="danger" @click="removeSlot(index)">删除</el-button>
        </div>
        <el-button type="primary" @click="addSlot">➕ 添加时间段</el-button>
      </div>

      <el-button type="success" @click="submit">提交设置</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import TopBar from '@/components/TopBar.vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import { useUserStore } from '@/stores/userStore'

const userStore = useUserStore()

const date = ref('')
const timeSlots = ref([
  { start: '', end: '', quota: 10 }
])

const addSlot = () => {
  timeSlots.value.push({ start: '', end: '', quota: 10 })
}
const removeSlot = (index) => {
  timeSlots.value.splice(index, 1)
}

const submit = async () => {
  if (!date.value || timeSlots.value.length === 0) {
    ElMessage.warning('请填写完整信息')
    return
  }

  const userId = localStorage.getItem('user_id')
  const role = localStorage.getItem('role')

  for (const slot of timeSlots.value) {
    if (!slot.start || !slot.end || !slot.quota) {
      ElMessage.warning('每个时间段都需要填写起始时间和号源量')
      return
    }

    const time_start = `${date.value}T${slot.start}:00`
    const time_end = `${date.value}T${slot.end}:00`

    try {
      const res = await axios.post('http://localhost:8000/doctor/create/', {
        user_id: userId,
        role: role,
        time_start: time_start,
        time_end: time_end,
        total_quota: slot.quota
      })

      if (res.data.code === 200) {
        ElMessage.success(`时间段 ${slot.start} - ${slot.end} 创建成功`)
      } else {
        ElMessage.error(res.data.message || '创建失败')
      }
    } catch (error) {
      ElMessage.error('服务器连接失败')
    }
  }
}
</script>

<style scoped>
.setting-page {
  padding-top: 120px;
  background: #eef3f5;
  min-height: 100vh;
}
.card {
  width: 700px;
  margin: 0 auto;
  padding: 30px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 16px;
}
.slot-row {
  display: flex;
  align-items: center;
  gap: 12px;
}
input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
}
</style>
