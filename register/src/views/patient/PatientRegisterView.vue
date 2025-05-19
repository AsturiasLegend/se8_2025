<!-- PatientRegisterView.vue -->
<template>
  <div class="register-wrapper">
    <!-- 顶栏 -->
    <TopBar title="XXX医院线上挂号系统" />

    <!-- 内容 -->
    <div class="register-content">
      <!-- 左侧表单 -->
      <div class="form-section">
        <h1 class="title">挂号</h1>
        <p class="subtitle">🛈 操作指引</p>
        <div class="dashed-divider"></div>

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

            <!-- 提交按钮 -->
            <button type="submit" class="submit-btn">提交挂号</button>
            </form>
      </div>

      <!-- 右侧日历 -->
      <div class="calendar-section">
        <!-- 示例图片 -->
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

const selectedDate = ref('') // 用于绑定选择的日期
const symptom = ref('')
const description = ref('')
const department = ref('')
const doctor = ref('')
const timeSlot = ref('')

const submitForm = () => {
  console.log('提交数据：', {
    symptom: symptom.value,
    description: description.value,
    department: department.value,
    doctor: doctor.value,
    timeSlot: timeSlot.value,
    date: selectedDate.value
  })
  alert('挂号信息已提交！')
}
</script>

<style scoped>
.register-wrapper {
  font-family: Arial, sans-serif;
}

.register-content {
  margin-top: 100px; /* ✅ 避开 fixed 顶栏 */
  display: flex;
  justify-content: space-between;
  padding: 40px 60px;
}

.form-section {
  flex: 1;
  padding-right: 40px;
  align-items: center; /* 左右居中对齐 */
}

.title {
  font-size: 28px;
  background-color: #0056ba;
  color: white;
  padding: 10px 40px;
  border-radius: 10px;
  display: inline-block;
  margin-bottom: 6px;
}

.subtitle {
  color: #666;
  font-size: 14px;
  margin-bottom: 16px;
}

.dashed-divider {
  border-bottom: 3px dashed #0056ba;
  margin: 16px 0 24px 0;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 100%; /* 全宽度，确保按钮居中 */
}

.register-form label {
  display: flex;
  flex-direction: column;
  font-size: 16px;
  color: #333;
}

input, textarea {
  margin-top: 6px;
  padding: 10px;
  border: 2px solid #666;
  border-radius: 4px;
  font-size: 14px;
  resize: none;
}

/* 日历区域 */
.calendar-section {
  flex: 1;
  padding-left: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column; /* ⬅️ 垂直排列 */
  gap: 50px; /* 图片与日历之间间距 */
  margin-top: 80px; 
}

.calendar-placeholder {
  width: 100%;
  height: 420px;
  border: 3px solid #0056ba;
  border-radius: 10px;
  text-align: center;
  padding-top: 60px;
  color: #666;
  background: white;
  font-size: 20px;
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
  align-self: center; /* 居中对齐 */
}
.submit-btn:hover {
  background-color: #0056ba;
}
</style>
