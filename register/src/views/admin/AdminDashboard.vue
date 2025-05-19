<template>
  <div class="admin-wrapper">
    <TopBar title="管理员控制台" />
    <div class="admin-content">
      <el-card class="panel" @click="goSchedule">
        <h3>📅 科室号源调控</h3>
        <p>管理每日号源与时间段设置</p>
      </el-card>

      <el-card class="panel" @click="goApproval">
        <h3>👨‍⚕️ 医生权限审批</h3>
        <p>处理医生权限变更和异常申请</p>
      </el-card>

      <el-card class="panel" @click="goMonitor">
        <h3>📊 系统运行状态监控</h3>
        <p>查看号源使用率、爽约率等</p>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import TopBar from '@/components/TopBar.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const goSchedule = () => router.push('/administrator/schedule')
const goApproval = () => router.push('/administrator/approval')
const goMonitor = () => router.push('/administrator/monitor')
</script>

<style scoped>
.admin-content {
  display: flex;
  justify-content: center;
  gap: 40px;
  padding: 60px;
  margin-top: 240px; /* ✅ 添加这句，避开 TopBar */
}
.panel {
  width: 220px;
  cursor: pointer;
  text-align: center;
  transition: box-shadow 0.3s;
}
.panel:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}
</style>
