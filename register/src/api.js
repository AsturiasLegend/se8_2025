import axios from 'axios'

const instance = axios.create({
  baseURL: 'http://localhost:8000/api', // Django 后端地址
  withCredentials: true // 如果使用 cookie 登录
})

export default instance