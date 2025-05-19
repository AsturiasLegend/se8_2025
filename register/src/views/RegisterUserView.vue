<template>
  <div class="register-page">
    <TopBar title="用户注册" />

    <div class="register-card">
      <h2>创建新账号</h2>
      <div class="form-group">
        <input type="text" v-model="username" placeholder="用户名" />
        <input type="text" v-model="name" placeholder="姓名" />
        
        <!-- 手机号码 (新增) -->
        <input type="text" v-model="phone" placeholder="手机号码" />
        
        <!-- 身份证号 (新增，可选) -->
        <input type="text" v-model="idCard" placeholder="身份证号 (选填)" />

        <!-- 性别下拉 -->
        <select v-model="gender">
          <option value="" disabled>请选择性别</option>
          <option value="男">男</option>
          <option value="女">女</option>
        </select>

        <!-- 年龄下拉 -->
        <select v-model="age">
          <option value="" disabled>请选择年龄</option>
          <option v-for="n in 100" :key="n" :value="n">{{ n }}</option>
        </select>

        <input type="password" v-model="password" placeholder="密码" />
        <input type="password" v-model="confirm" placeholder="确认密码" />
      </div>

      <button class="register-btn" @click="submit">注册</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import TopBar from '@/components/TopBar.vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import axios from 'axios'

const username = ref('')
const name = ref('')
const phone = ref('') // 新增手机号码字段
const idCard = ref('') // 新增身份证号字段（可选）
const gender = ref('')
const age = ref('')
const password = ref('')
const confirm = ref('')
const router = useRouter()

const submit = async () => {
  // 检查必填字段
  if (!username.value || !name.value || !phone.value || !gender.value || !age.value || !password.value || !confirm.value) {
    ElMessage.warning('请填写所有必填字段')
    return
  }
  
  // 简化验证：仅验证手机号长度
  if (phone.value.length !== 11) {
    ElMessage.error('手机号必须为11位')
    return
  }
  
  // 简化验证：如果填写了身份证号，只验证长度（18位）
  if (idCard.value && idCard.value.length !== 18) {
    ElMessage.error('身份证号必须为18位')
    return
  }
  
  // 验证密码一致性
  if (password.value !== confirm.value) {
    ElMessage.error('两次输入密码不一致')
    return
  }

  try {
    const res = await axios.post('http://localhost:8000/register/', {
      username: username.value,
      real_name: name.value,
      phone: phone.value,
      id_card: idCard.value || null, // 如果为空，发送null
      gender: gender.value === '男' ? 'M' : 'F',
      age: age.value,
      password: password.value,
      role: 'patient' // ✅ 固定为患者注册
    })

    if (res.data.status === 'success') {
      ElMessageBox.alert('注册成功！点击确定返回首页', '注册成功', {
        confirmButtonText: '确定',
        callback: () => {
          router.push('/entry')
        }
      })
    } else {
      ElMessage.error(res.data.message || '注册失败')
    }
  } catch (e) {
    console.error(e.response?.data || e)
    ElMessage.error(e.response?.data?.message || '服务器连接失败')
  }
}
</script>

<style scoped>
.register-page {
  padding-top: 120px;
  background: #eef3f5;
  height: 100vh;
}
.register-card {
  background: white;
  width: 360px;
  margin: 0 auto;
  padding: 40px;
  border-radius: 16px;
  text-align: center;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}
h2 {
  margin-bottom: 24px;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 20px;
}
input {
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
}
select {
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
  background-color: white;
}
.register-btn {
  background: #0056ba;
  color: white;
  font-size: 16px;
  padding: 12px;
  width: 100%;
  border-radius: 8px;
  border: none;
  cursor: pointer;
}
</style>