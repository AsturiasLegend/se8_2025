<template>
  <div class="help-page">
    <TopBar title="医生帮助" />

    <div class="card">
      <h2>使用教程 - 医生端</h2>

      <p>1. 登录系统后进入接诊管理页面查看待就诊患者。</p>
      <p>2. 点击“提前接诊”或“完成接诊”按钮进行患者接诊流程。</p>
      <p>3. 可在“报告异常”中填写诊疗过程中的异常情况。</p>
      <p>4. 在“号源设置”中添加自己可接诊的时间段及数量。</p>
      <p>5. 可通过“医生信息”页面查看并编辑个人简介。</p>
      <p>6. 如遇问题可联系管理员协助处理。</p>
    </div>
  </div>
</template>

<script setup>
import TopBar from '@/components/TopBar.vue'
</script>

<style scoped>
.help-page {
  padding-top: 120px;
  background: #f5f7fa;
  min-height: 100vh;
}

.card {
  width: 720px;
  margin: 0 auto;
  padding: 30px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-bottom: 20px;
  color: #333;
}

p {
  margin-bottom: 10px;
  line-height: 1.6;
}
</style>
