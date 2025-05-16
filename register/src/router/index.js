import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import UserDashboard from '../views/UserDashboard.vue'
import PatientRegisterView from '../views/PatientRegisterView.vue'
import EntryView from '../views/EntryView.vue'
import DoctorDashboard from '../views/DoctorDashboard.vue'
import RegisterUserView from '../views/RegisterUserView.vue'
import AdminDashboard from '../views/AdminDashboard.vue'

const routes = [
    {
        path: '/',
        redirect: '/entry'  // ⬅ 登录页变成默认页
      },
    { 
        path: '/entry', 
        name: 'Entry', 
        component: EntryView 
      },
    {
        path: '/login',
        name: 'Login',
        component: LoginView
      },
      {
        path: '/dashboard',
        name: 'Dashboard',
        component: UserDashboard
      },
      {
        path: '/register',
        name: 'Register',
        component: PatientRegisterView
      },
    { path: '/doctor', 
        name: 'Doctor', 
        component: DoctorDashboard 
    },
    {
        path: '/register-user',
        name: 'RegisterUser',
        component: RegisterUserView
      },
    { 
        path: '/admin', 
        name: 'Admin', 
        component: AdminDashboard
      }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
