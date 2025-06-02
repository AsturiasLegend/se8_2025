<template>
  <div class="approval-wrapper">
    <TopBar title="医生权限审批" />
    <div class="approval-content">
      <!-- 筛选表单 -->
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
          <el-form-item label="状态">
            <el-select v-model="filterForm.status" placeholder="选择状态">
              <el-option label="待审批" value="pending" />
              <el-option label="已通过" value="approved" />
              <el-option label="已拒绝" value="rejected" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">查询</el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <!-- 审批列表 -->
      <el-card class="approval-card">
        <el-table :data="approvals" style="width: 100%">
          <el-table-column prop="doctor_name" label="医生姓名" width="120" />
          <el-table-column prop="department_name" label="申请科室" width="120" />
          <el-table-column prop="is_primary" label="是否主科室" width="100">
            <template #default="scope">
              <el-tag :type="scope.row.is_primary ? 'success' : 'info'">
                {{ scope.row.is_primary ? '是' : '否' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getStatusType(scope.row.status)">
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="申请时间" width="180">
            <template #default="scope">
              {{ formatDate(scope.row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template #default="scope">
              <el-button
                v-if="scope.row.status === 'pending'"
                size="small"
                type="success"
                @click="handleApprove(scope.row)"
              >
                通过
              </el-button>
              <el-button
                v-if="scope.row.status === 'pending'"
                size="small"
                type="danger"
                @click="handleReject(scope.row)"
              >
                拒绝
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import TopBar from '@/components/TopBar.vue'
import api from '@/api'

// 数据
const departments = ref([])
const approvals = ref([])
const filterForm = ref({
  departmentId: '',
  status: 'pending'
})

// 方法
const loadDepartments = async () => {
  try {
    const response = await api.get('/admin/departments/')
    departments.value = response.data
  } catch (error) {
    ElMessage.error('加载科室列表失败')
  }
}

const loadApprovals = async () => {
  try {
    const params = {}
    if (filterForm.value.departmentId) {
      params.department_id = filterForm.value.departmentId
    }
    if (filterForm.value.status) {
      params.status = filterForm.value.status
    }
    const response = await api.get('/admin/doctor-departments/', { params })
    approvals.value = response.data
  } catch (error) {
    ElMessage.error('加载审批列表失败')
  }
}

const handleSearch = () => {
  loadApprovals()
}

const handleApprove = async (row) => {
  try {
    await ElMessageBox.confirm('确定通过该医生的科室申请吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await api.patch(`/admin/doctor-departments/${row.id}/`, {
      status: 'approved'
    })
    ElMessage.success('已通过申请')
    loadApprovals()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败')
    }
  }
}

const handleReject = async (row) => {
  try {
    await ElMessageBox.confirm('确定拒绝该医生的科室申请吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await api.patch(`/admin/doctor-departments/${row.id}/`, {
      status: 'rejected'
    })
    ElMessage.success('已拒绝申请')
    loadApprovals()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败')
    }
  }
}

const getStatusType = (status) => {
  const types = {
    pending: 'warning',
    approved: 'success',
    rejected: 'danger'
  }
  return types[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    pending: '待审批',
    approved: '已通过',
    rejected: '已拒绝'
  }
  return texts[status] || status
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleString()
}

// 生命周期
onMounted(() => {
  loadDepartments()
  loadApprovals()
})
</script>

<style scoped>
.approval-wrapper {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.approval-content {
  padding: 20px;
  margin-top: 60px;
}

.filter-card {
  margin-bottom: 20px;
}

.approval-card {
  margin-bottom: 20px;
}
</style> 