<template>
  <div>
    <TopBar />

    <!-- ✅ 添加背景图模糊容器 -->
    <div class="login-page">
      <div class="bg-blur-overlay"></div>

      <!-- 登录卡片在上面 -->
      <div class="login-card">
        <img class="avatar" src="../assets/avatar.png" alt="avatar" />
        <h2>欢迎回来</h2>

        <div class="form-group">
          <input type="text" placeholder="用户名" v-model="username" />
          <input type="password" placeholder="密码" v-model="password" />
        </div>

        <button class="login-btn" @click="handleLogin">登录</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import TopBar from '../components/TopBar.vue'
import { useUserStore } from '../stores/userStore'  // ✅ 路径根据实际位置调整
const userStore = useUserStore()
const router = useRouter()
const route = useRoute()
const username = ref('')
const password = ref('')
const role = route.query.role || 'patient'  // ✅ 角色参数从路由参数获取

const handleLogin = async () => {
   try {
     const res = await axios.post('http://localhost:8000/login/', {
       username: username.value,
       password: password.value,
       role: role
     })

     if (res.data.status === 'success') {
        // ✅ 设置用户状态（可用于权限控制）
        const userRole = res.data.user_info.role  // 这里改为使用后端返回的角色信息进行跳转
        userStore.setUser({
            username: username.value,
            role: userRole,
            token: res.data.token
        })
        localStorage.setItem('user_id', res.data.user_info.id)
        localStorage.setItem('role', res.data.user_info.role)


       ElMessage.success('登录成功')
        if (res.data.user_info.role === 'doctor')
           router.push('/doctor/dashboard')
        else if (userRole === 'administrator')
           router.push('/administrator/dashboard')
        else
           router.push('/patient/dashboard')
     } else {
       ElMessage.error(res.data.message || '用户名或密码错误')
     }
   } catch (error) {
           if (error.response) {
      // 服务器返回了 4xx/5xx 响应
      const status = error.response.status;
      
      // 根据状态码显示不同错误
      if (status === 400) {
        ElMessage.error('用户名或密码错误');
      } else if (status === 500) {
        ElMessage.error('服务器内部错误');
      } else {
        ElMessage.error(`请求失败（错误码：${status}）`);
      }

    } else {
      // 网络错误（无法连接服务器）
      ElMessage.error('无法连接服务器');
    }
   }
 }
</script>

<style scoped>
.login-page {
  height: calc(100vh - 150px); /* 扣除顶栏高度 */
  display: flex;
  justify-content: center;
  align-items: center;
  background: #eef3f5 url('../assets/hospital-building.png') no-repeat center center;
  /* background: #eef3f5; */
  background-size: cover;
  overflow: hidden;
}
/* ✅ 模糊遮罩层 */
.bg-blur-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  backdrop-filter: blur(8px);
  background-color: rgba(255, 255, 255, 0.3); /* 加一点透明白提升亮度 */
  z-index: 1;
}
.login-card {
  position: relative;
  z-index: 2;
  width: 320px;
  padding: 40px 30px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 16px;
}

h2 {
  margin-bottom: 24px;
  color: #333;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 24px;
}

input {
  padding: 12px 16px;
  font-size: 16px;
  border-radius: 8px;
  border: 1px solid #ccc;
  outline: none;
  transition: border 0.3s;
}

input:focus {
  border-color: #409eff;
}

.login-btn {
  padding: 12px;
  width: 100%;
  background: #007bff;
  border: none;
  color: white;
  font-size: 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s;
}

.login-btn:hover {
  background: #0056c5;
}
</style>
