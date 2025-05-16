<template>
  <header class="top-bar">
    <div class="logo">
      🏥 XXX医院线上挂号系统
    </div>
    <div class="user-icon">
      👤
    </div>
  </header>
</template>

<style scoped>
.top-bar {
  height: 60px;
  background-color: #0056ba;
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100px;
  padding: 12 20px;
  font-size: 40px;
  font-weight: bold;
  position: fixed;         /* ✅ 固定在页面顶部 */
  top: 0;
  left: 0;
  right: 0;
  z-index: 999;            /* ✅ 最高层级，确保不被遮罩层盖住 */
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-icon {
  font-size: 24px;
  cursor: pointer;
}
</style>
