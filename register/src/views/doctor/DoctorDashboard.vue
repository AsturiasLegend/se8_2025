<template>
  <div class="doctor-wrapper">
    <TopBar title="医生工作台" />

    <div class="content">
      <h2>📋 我的挂号病人</h2>

      <!-- ✅ 表格包裹容器，启用滚动 -->
      <div class="table-wrapper">
        <el-table
          :data="patients"
          border
          style="width: 100%"
          @selection-change="handleSelectionChange"
        >
          <el-table-column type="selection" width="55" />
          <el-table-column prop="name" label="姓名" width="120" />
          <el-table-column prop="gender" label="性别" width="80" />
          <el-table-column prop="age" label="年龄" width="80" />
          <el-table-column prop="symptom" label="病症描述" />
          <el-table-column prop="time" label="挂号时间段" width="300" />
        </el-table>
      </div>

      <!-- ✅ 操作按钮 -->
      <div class="button-row">
        <el-button type="primary" :disabled="!selectedPatient" @click="callPatient">叫号</el-button>
        <el-button type="success" :disabled="!selectedPatient" @click="finishPatient">接诊完成</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import TopBar from '@/components/TopBar.vue'
import { ElMessage } from 'element-plus'

const patients = ref([
  { id: 1, name: '张三', gender: '男', age: 32, symptom: '发烧、咳嗽', time: '2025-04-18 上午 9:00 - 10:00' },
  { id: 2, name: '李四', gender: '女', age: 28, symptom: '头痛', time: '2025-04-18 上午 10:00 - 11:00' },
  { id: 3, name: '王五', gender: '男', age: 45, symptom: '腹痛', time: '2025-04-18 下午 2:00 - 3:00' }

])

const selectedPatient = ref(null)

const handleSelectionChange = (selection) => {
  selectedPatient.value = selection[0] || null
}

const callPatient = () => {
  if (selectedPatient.value) {
    ElMessage.info(`🔔 请 ${selectedPatient.value.name} 到诊室就诊`)
  }
}

const finishPatient = () => {
  if (selectedPatient.value) {
    ElMessage.success(`✅ 已完成 ${selectedPatient.value.name} 的接诊`)
    patients.value = patients.value.filter(p => p.id !== selectedPatient.value.id)
    selectedPatient.value = null
  }
}
</script>

<style scoped>
.doctor-wrapper {
  font-family: Arial, sans-serif;
}
.content {
  padding: 40px;
  padding-top: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
h2 {
  margin-bottom: 20px;
}

/* ✅ 滚动表格容器 */
.table-wrapper {
  max-height: 400px;
  overflow-y: auto;
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* ✅ 表格样式 */
.el-table {
  width: 100%;
}

/* ✅ 中间对齐按钮 */
.button-row {
  margin-top: 24px;
  display: flex;
  gap: 20px;
  justify-content: center;
}
</style>
