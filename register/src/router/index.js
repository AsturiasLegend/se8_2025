import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/userStore' // ✅ 引入 pinia 状态管理
import { ElMessage } from 'element-plus'

// 页面组件导入
import EntryView from '@/views/EntryView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterUserView from '@/views/RegisterUserView.vue'
import UserDashboard from '@/views/patient/PatientDashboard.vue'
import PatientRegisterView from '@/views/patient/PatientRegisterView.vue'
import DoctorDashboard from '@/views/doctor/DoctorDashboard.vue'
import DiagnosisList from '@/views/doctor/DiagnosisList.vue'
import AppointmentSetting from '@/views/doctor/AppointmentSetting.vue'
import AdminDashboard from '@/views/admin/AdminDashboard.vue'
import DoctorProfile from '@/views/doctor/DoctorProfile.vue'
import DoctorHelp from '@/views/doctor/DoctorHelp.vue'
import PatientHelp from '@/views/patient/PatientHelp.vue'
import PatientProfile from '@/views/patient/PatientProfile.vue'

const routes = [
  { path: '/', redirect: '/entry' },

  // 公共页面
  { path: '/entry', name: 'Entry', component: EntryView },
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/register-user', name: 'RegisterUser', component: RegisterUserView },

  // 患者页面
  { path: '/patient/dashboard', name: 'PatientDashboard', component: UserDashboard },
  { path: '/patient/register', name: 'PatientRegister', component: PatientRegisterView },
  { path: '/patient/help', name: 'PatientHelp', component: PatientHelp},
  { path: '/patient/profile', name: 'PatientProfile', component: PatientProfile },

  // 医生页面
  { path: '/doctor/dashboard', name: 'DoctorDashboard', component: DoctorDashboard },
  { path: '/doctor/diagnosislist', name: 'DiagnosisList', component: DiagnosisList },
  { path: '/doctor/appointmentsetting', name: 'AppointmentSetting', component: AppointmentSetting},
  { path: '/doctor/profile', name: 'DoctorProfile', component: DoctorProfile },
  { path: '/doctor/help', name: 'DoctorHelp', component: DoctorHelp},

  // 管理员页面
  { path: '/administrator/dashboard', name: 'AdminDashboard', component: AdminDashboard }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  const role = userStore.role
  const isLoggedIn = !!role

  const rolePrefixMap = {
    patient: '/patient/',
    doctor: '/doctor/',
    administrator: '/administrator/'
  }

  const path = to.path
  const isProtectedPath = Object.values(rolePrefixMap).some(prefix => path.startsWith(prefix))

  if (isProtectedPath) {
    if (!isLoggedIn) {
      // ❌ 未登录，弹窗提醒，并跳转入口页
      ElMessage.warning('请先登录以访问该功能')
      return next('/entry')
    }

    const allowedPrefix = rolePrefixMap[role]
    if (!path.startsWith(allowedPrefix)) {
      // ❌ 已登录但角色不匹配，弹窗提醒并跳转入口页
      ElMessage.error('无权限访问该页面')
      return next('/entry')
    }
  }

  next() // ✅ 放行公共页面
})

export default router
