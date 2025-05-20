<template>
  <div class="register-page">
    <TopBar title="用户注册" />

    <div class="register-card">
      <h2>创建新账号</h2>
      <div class="form-group">
        <input type="text" v-model="username" placeholder="用户名" />
        <input type="text" v-model="name" placeholder="姓名" />
        
        <!-- ✅ 性别下拉 -->
        <select v-model="gender">
          <option value="" disabled>请选择性别</option>
          <option value="男">男</option>
          <option value="女">女</option>
        </select>

        <!-- ✅ 年龄下拉 -->
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

const username = ref('')
const name = ref('')
const gender = ref('')
const age = ref('')
const password = ref('')
const confirm = ref('')
const router = useRouter()

const submit = async () => {
  if (!username.value || !name.value || !gender.value || !age.value || !password.value || !confirm.value) {
    ElMessage.warning('请填写所有字段')
    return
  }
  if (password.value !== confirm.value) {
    ElMessage.error('两次输入密码不一致')
    return
  }
  ElMessageBox.alert('注册成功！点击确定返回首页', '注册成功', {
    confirmButtonText: '确定',
    callback: () => {
      router.push('/')
    }
  })

//   try {
//     const res = await fetch('http://localhost:8000/register/', {
//       method: 'POST',
//       headers: { 'Content-Type': 'application/json' },
//       body: JSON.stringify({
//         username: username.value,
//         name: name.value,
//         gender: gender.value,
//         age: age.value,
//         password: password.value
//       })
//     })
//     const data = await res.json()
//     if (data.status === 'success') {
//       ElMessageBox.alert('注册成功！点击确定返回首页', '注册成功', {
//       confirmButtonText: '确定',
//       callback: () => {
//         router.push('/')
//       }
//   })
//     } else {
//       ElMessage.error(data.message || '注册失败')
//     }
//   } catch (e) {
//     ElMessage.error('服务器连接失败')
//   }
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
select {
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
  background-color: white;
}
</style>
