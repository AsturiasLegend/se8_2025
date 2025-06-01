<template>
  <div class="help-wrapper">
    <TopBar title="系统帮助" />

    <div class="content-box">
      <h2 class="help-title">🛈 使用帮助 - 患者端</h2>
      <div class="help-content">
        <p>1. 登录后进入患者主页，可查看挂号记录与挂号入口。</p>
        <p>2. 点击“去挂号”可选择科室、医生、时间段，完成挂号。</p>
        <p>3. 可在日历中选择预约日期，并填写症状信息。</p>
        <p>4. 提交后可在主页查看您的挂号记录，等待就诊。</p>
        <p>5. 点击用户名旁的“退出”按钮可安全登出系统。</p>
        <p>6. 如果遇到系统问题，请联系管理员或刷新页面。</p>
        <p>7. 本系统仅作为挂号模拟，数据不做真实存储用途。</p>
        <p>8. 如有更多建议或反馈，可发送邮件至 support@example.com。</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import TopBar from '@/components/TopBar.vue'
</script>

<style scoped>
.help-wrapper {
  padding-top: 120px;
  background: #eef3f5;
  min-height: 100vh;
  font-family: Arial, sans-serif;
}

.content-box {
  width: 700px;
  margin: 0 auto;
  padding: 30px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
  max-height: 600px;
  overflow-y: auto;
}

.help-title {
  font-size: 22px;
  color: #0056ba;
  margin-bottom: 20px;
  font-weight: bold;
}

.help-content {
  font-size: 16px;
  color: #333;
  line-height: 1.8;
}
</style>
