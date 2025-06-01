<template>
  <div class="register-wrapper">
    <TopBar title="XXX医院线上挂号系统" />

    <div class="register-content">
      <div class="form-section">
        <h1 class="title">挂号</h1>

        <form class="register-form" @submit.prevent="submitForm">
          <label>您的简要病症：
            <input type="text" v-model="symptom" />
          </label>

          <label>描述您的病情：
            <textarea rows="4" v-model="description" />
          </label>

          <label>*选择科室：
            <el-select v-model="department" placeholder="请选择科室">
              <el-option label="内科" value="内科" />
              <el-option label="外科" value="外科" />
              <el-option label="儿科" value="儿科" />
            </el-select>
          </label>

          <label>*选择医生：
            <el-select v-model="doctor" placeholder="请选择医生">
              <el-option label="张医生" value="张医生" />
              <el-option label="李医生" value="李医生" />
            </el-select>
          </label>

          <label>*选择时间段：
            <el-select v-model="timeSlot" placeholder="请选择时间段">
              <el-option label="上午 8:00-10:00" value="morning" />
              <el-option label="下午 14:00-16:00" value="afternoon" />
            </el-select>
          </label>

          <button type="submit" class="submit-btn">提交挂号</button>
        </form>
      </div>

      <div class="calendar-section">
        <img class="calendar-demo-img" src="../../assets/calendar-example.png" alt="示例日历" />
        <el-date-picker
          v-model="selectedDate"
          type="date"
          placeholder="选择日期"
          size="large"
          style="width: 300px"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import TopBar from '@/components/TopBar.vue'
import { ref } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const selectedDate = ref('')
const symptom = ref('')
const description = ref('')
const department = ref('')
const doctor = ref('')
const timeSlot = ref('')

const submitForm = async () => {
  const userId = localStorage.getItem('user_id')
  const role = localStorage.getItem('role')

  if (!selectedDate.value || !department.value || !doctor.value || !timeSlot.value) {
    ElMessage.warning('请完整填写所有必填项')
    return
  }

  try {
    const res = await axios.post('http://localhost:8000/patient/register/', {
      user_id: userId,
      role: role,
      symptom: symptom.value,
      description: description.value,
      department: department.value,
      doctor: doctor.value,
      time_slot: timeSlot.value,
      date: selectedDate.value
    })

    if (res.data.code === 200) {
      ElMessage.success('挂号成功')
    } else {
      ElMessage.error(res.data.message || '挂号失败')
    }
  } catch (error) {
    ElMessage.error('服务器连接失败')
  }
}
</script>

<style scoped>
.register-wrapper {
  font-family: Arial, sans-serif;
}

.register-content {
  margin-top: 100px;
  display: flex;
  justify-content: space-between;
  padding: 40px 60px;
}

.form-section {
  flex: 1;
  padding-right: 40px;
}

.title {
  font-size: 28px;
  background-color: #0056ba;
  color: white;
  padding: 10px 40px;
  border-radius: 10px;
  display: inline-block;
  margin-bottom: 16px;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 100%;
}

.register-form label {
  display: flex;
  flex-direction: column;
  font-size: 16px;
  color: #333;
}

input,
textarea {
  margin-top: 6px;
  padding: 10px;
  border: 2px solid #666;
  border-radius: 4px;
  font-size: 14px;
  resize: none;
}

.calendar-section {
  flex: 1;
  padding-left: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 50px;
  margin-top: 20px;
}

.submit-btn {
  margin-top: 50px;
  padding: 12px;
  width: 50%;
  background-color: #007bff;
  color: white;
  font-size: 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s;
  align-self: center;
}
.submit-btn:hover {
  background-color: #0056ba;
}
</style>
