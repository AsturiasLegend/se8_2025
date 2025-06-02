<template>
  <div class="monitor-wrapper">
    <TopBar title="系统运行状态监控" />
    <div class="monitor-content">
      <!-- 总体指标卡片 -->
      <el-row :gutter="20" class="metric-cards">
        <el-col :span="6">
          <el-card shadow="hover">
            <template #header>
              <div class="card-header">
                <span>总预约数</span>
              </div>
            </template>
            <div class="metric-value">{{ metrics.total || 0 }}</div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover">
            <template #header>
              <div class="card-header">
                <span>已完成预约</span>
              </div>
            </template>
            <div class="metric-value">{{ metrics.completed || 0 }}</div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover">
            <template #header>
              <div class="card-header">
                <span>已取消预约</span>
              </div>
            </template>
            <div class="metric-value">{{ metrics.canceled || 0 }}</div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover">
            <template #header>
              <div class="card-header">
                <span>爽约数</span>
              </div>
            </template>
            <div class="metric-value">{{ metrics.no_show || 0 }}</div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 科室统计表格 -->
      <el-card class="department-stats">
        <template #header>
          <div class="card-header">
            <span>科室预约统计</span>
          </div>
        </template>
        <el-table :data="departmentStats" style="width: 100%">
          <el-table-column prop="department__name" label="科室" />
          <el-table-column prop="total" label="总排班数" />
          <el-table-column prop="remaining" label="剩余号量" />
          <el-table-column label="使用率">
            <template #default="scope">
              {{ calculateUsageRate(scope.row) }}%
            </template>
          </el-table-column>
        </el-table>
      </el-card>

      <!-- 每日指标图表 -->
      <el-card class="daily-metrics">
        <template #header>
          <div class="card-header">
            <span>每日预约指标</span>
          </div>
        </template>
        <div ref="chartRef" style="width: 100%; height: 400px"></div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import TopBar from '@/components/TopBar.vue'
import api from '@/api'
import * as echarts from 'echarts'

// 数据
const metrics = ref({})
const departmentStats = ref([])
const dailyMetrics = ref([])
const chartRef = ref(null)
let chart = null

// 方法
const loadDashboardData = async () => {
  try {
    const response = await api.get('/admin/system-metrics/dashboard/')
    metrics.value = response.data.overall_metrics
    departmentStats.value = response.data.department_stats
    dailyMetrics.value = response.data.daily_metrics
    updateChart()
  } catch (error) {
    ElMessage.error('加载监控数据失败')
  }
}

const calculateUsageRate = (row) => {
  if (!row.total) return 0
  return Math.round(((row.total - row.remaining) / row.total) * 100)
}

const updateChart = () => {
  if (!chart) {
    chart = echarts.init(chartRef.value)
  }

  const option = {
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['总预约数', '已完成', '已取消', '爽约数']
    },
    xAxis: {
      type: 'category',
      data: dailyMetrics.value.map(item => item.date)
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '总预约数',
        type: 'line',
        data: dailyMetrics.value.map(item => item.total_appointments)
      },
      {
        name: '已完成',
        type: 'line',
        data: dailyMetrics.value.map(item => item.completed_appointments)
      },
      {
        name: '已取消',
        type: 'line',
        data: dailyMetrics.value.map(item => item.canceled_appointments)
      },
      {
        name: '爽约数',
        type: 'line',
        data: dailyMetrics.value.map(item => item.no_show_appointments)
      }
    ]
  }

  chart.setOption(option)
}

// 生命周期
onMounted(() => {
  loadDashboardData()
  // 每5分钟刷新一次数据
  const timer = setInterval(loadDashboardData, 5 * 60 * 1000)
  onUnmounted(() => {
    clearInterval(timer)
    if (chart) {
      chart.dispose()
    }
  })
})
</script>

<style scoped>
.monitor-wrapper {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.monitor-content {
  padding: 20px;
  margin-top: 60px;
}

.metric-cards {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.metric-value {
  font-size: 24px;
  font-weight: bold;
  text-align: center;
  color: #409EFF;
}

.department-stats {
  margin-bottom: 20px;
}

.daily-metrics {
  margin-bottom: 20px;
}
</style> 