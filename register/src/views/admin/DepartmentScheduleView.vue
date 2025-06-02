<template>
  <div class="schedule-wrapper">
    <TopBar title="科室号源调控" />
    <div class="schedule-content">
      <el-card class="filter-card">
        <el-form :inline="true" :model="filterForm">
          <el-form-item label="科室">
            <el-select v-model="filterForm.departmentId" placeholder="选择科室">
              <el-option
                v-for="dept in departments"
                :key="dept.id"
                :label="dept.name"
                :value="dept.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="日期">
            <el-date-picker
              v-model="filterForm.date"
              type="date"
              placeholder="选择日期"
              :disabled-date="disabledDate"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">查询</el-button>
            <el-button type="success" @click="handleAdd">新增排班</el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <el-card class="schedule-card">
        <el-table :data="schedules" style="width: 100%">
          <el-table-column prop="department_name" label="科室" width="180" />
          <el-table-column prop="date" label="日期" width="180">
            <template #default="scope">
              {{ formatDate(scope.row.date) }}
            </template>
          </el-table-column>
          <el-table-column prop="time_slot" label="时间段" width="180">
            <template #default="scope">
              {{ formatTime(scope.row.time_slot) }}
            </template>
          </el-table-column>
          <el-table-column prop="total_quota" label="总号量" width="120" />
          <el-table-column prop="remaining_quota" label="剩余号量" width="120" />
          <el-table-column prop="is_active" label="状态" width="120">
            <template #default="scope">
              <el-tag :type="scope.row.is_active ? 'success' : 'danger'">
                {{ scope.row.is_active ? '启用' : '停用' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template #default="scope">
              <el-button
                size="small"
                :type="scope.row.is_active ? 'danger' : 'success'"
                @click="handleToggleStatus(scope.row)"
              >
                {{ scope.row.is_active ? '停用' : '启用' }}
              </el-button>
              <el-button
                size="small"
                type="primary"
                @click="handleEdit(scope.row)"
              >
                编辑
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>

      <!-- 新增/编辑对话框 -->
      <el-dialog
        :title="dialogTitle"
        v-model="dialogVisible"
        width="500px"
      >
        <el-form :model="scheduleForm" label-width="100px">
          <el-form-item label="科室">
            <el-select v-model="scheduleForm.department_id" placeholder="选择科室">
              <el-option
                v-for="dept in departments"
                :key="dept.id"
                :label="dept.name"
                :value="dept.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="日期">
            <el-date-picker
              v-model="scheduleForm.date"
              type="date"
              placeholder="选择日期"
              :disabled-date="disabledDate"
            />
          </el-form-item>
          <el-form-item label="时间段">
            <el-time-picker
              v-model="scheduleForm.time_slot"
              format="HH:mm"
              placeholder="选择时间"
            />
          </el-form-item>
          <el-form-item label="总号量">
            <el-input-number v-model="scheduleForm.total_quota" :min="1" />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="handleSubmit">确定</el-button>
          </span>
        </template>
      </el-dialog>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import TopBar from '@/components/TopBar.vue'
import api from '@/api'

// 数据
const departments = ref([])
const schedules = ref([])
const filterForm = ref({
  departmentId: '',
  date: new Date()
})
const scheduleForm = ref({
  department_id: '',
  date: new Date(),
  time_slot: '',
  total_quota: 20
})
const dialogVisible = ref(false)
const dialogTitle = ref('新增排班')
const isEdit = ref(false)

// 方法
const loadDepartments = async () => {
  try {
    const response = await api.get('/admin/departments/')
    departments.value = response.data
  } catch (error) {
    ElMessage.error('加载科室列表失败')
  }
}

const loadSchedules = async () => {
  try {
    const params = {}
    if (filterForm.value.departmentId) {
      params.department_id = filterForm.value.departmentId
    }
    if (filterForm.value.date) {
      params.date = formatDate(filterForm.value.date)
    }
    const response = await api.get('/admin/department-schedules/', { params })
    schedules.value = response.data
  } catch (error) {
    ElMessage.error('加载排班列表失败')
  }
}

const handleSearch = () => {
  loadSchedules()
}

const handleAdd = () => {
  isEdit.value = false
  dialogTitle.value = '新增排班'
  scheduleForm.value = {
    department_id: filterForm.value.departmentId,
    date: filterForm.value.date,
    time_slot: '',
    total_quota: 20
  }
  dialogVisible.value = true
}

const handleEdit = (row) => {
  isEdit.value = true
  dialogTitle.value = '编辑排班'
  scheduleForm.value = { ...row }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  try {
    if (isEdit.value) {
      await api.put(`/admin/department-schedules/${scheduleForm.value.id}/`, scheduleForm.value)
      ElMessage.success('更新成功')
    } else {
      await api.post('/admin/department-schedules/', scheduleForm.value)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadSchedules()
  } catch (error) {
    ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
  }
}

const handleToggleStatus = async (row) => {
  try {
    await api.patch(`/admin/department-schedules/${row.id}/`, {
      is_active: !row.is_active
    })
    ElMessage.success('状态更新成功')
    loadSchedules()
  } catch (error) {
    ElMessage.error('状态更新失败')
  }
}

const disabledDate = (time) => {
  return time.getTime() < Date.now() - 8.64e7
}

const formatDate = (date) => {
  if (!date) return ''
  const d = new Date(date)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

const formatTime = (time) => {
  if (!time) return ''
  return time.substring(0, 5)
}

// 生命周期
onMounted(() => {
  loadDepartments()
  loadSchedules()
})
</script>

<style scoped>
.schedule-wrapper {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.schedule-content {
  padding: 20px;
  margin-top: 60px;
}

.filter-card {
  margin-bottom: 20px;
}

.schedule-card {
  margin-bottom: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 