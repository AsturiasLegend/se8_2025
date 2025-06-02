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
            <el-select v-model="department" placeholder="请选择科室" @change="fetchDoctors">
              <el-option v-for="dept in departments" :key="dept" :label="dept" :value="dept" />
            </el-select>
          </label>

          <label>*选择医生：
            <el-select v-model="doctor" placeholder="请选择医生" @change="fetchSlots">
              <el-option v-for="doc in doctors" :key="doc.id" :label="doc.real_name" :value="doc.id" />
            </el-select>
          </label>

          <label>*选择日期：
            <el-date-picker
              v-model="selectedDate"
              type="date"
              placeholder="选择日期"
              size="large"
              style="width: 300px"
              @change="fetchSlots"
            />
          </label>

          <label>*选择时间段：
            <el-select v-model="selectedSlotId" placeholder="请选择时间段">
              <el-option
                v-for="slot in timeSlots"
                :key="slot.slot_id"
                :label="`${slot.start} - ${slot.end}`"
                :value="slot.slot_id"
              />
            </el-select>
          </label>

          <button type="submit" class="submit-btn">提交挂号</button>
        </form>
      </div>

      <div class="calendar-section">
        <img class="calendar-demo-img" src="../../assets/calendar-example.png" alt="示例日历" />
      </div>
    </div>
  </div>
</template>

<script setup>
import TopBar from '@/components/TopBar.vue'
import { ref } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const symptom = ref('')
const description = ref('')
const department = ref('')
const doctor = ref('')
const selectedDate = ref('')
const selectedSlotId = ref('')

const departments = ['内科', '外科', '儿科', '眼科']
const doctors = ref([])
const timeSlots = ref([])

const fetchDoctors = async () => {
  doctor.value = ''
  selectedSlotId.value = ''
  timeSlots.value = []

  try {
    const res = await axios.get('http://localhost:8000/patient/get_doctors/', {
      params: { department: department.value }
    })
    if (res.data.code === 200) {
      doctors.value = res.data.data
    } else {
      ElMessage.error(res.data.message || '获取医生失败')
    }
  } catch {
    ElMessage.error('服务器连接失败')
  }
}

const fetchSlots = async () => {
  if (!doctor.value || !selectedDate.value) return

  try {
    const res = await axios.get('http://localhost:8000/patient/get_slots/', {
      params: {
        doctor_id: doctor.value,
        date: selectedDate.value
      }
    })
    if (res.data.code === 200) {
      // 假设返回为 [{ slot_id, start, end }]
      timeSlots.value = res.data.data
    } else {
      ElMessage.error(res.data.message || '获取时间段失败')
    }
  } catch {
    ElMessage.error('服务器连接失败')
  }
}

const submitForm = async () => {
  const userId = localStorage.getItem('user_id')
  const role = localStorage.getItem('role')

  if (!department.value || !doctor.value || !selectedDate.value || !selectedSlotId.value) {
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
      doctor_id: doctor.value,
      slot_id: selectedSlotId.value
    })

    if (res.data.code === 200) {
      ElMessage.success('挂号成功')
    } else {
      ElMessage.error(res.data.message || '挂号失败')
    }
  } catch {
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
