<template>
  <div class="container mx-auto px-4 py-8">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-2">แดชบอร์ด</h1>
      <p class="text-gray-600">ภาพรวมระบบจัดการการประชุม</p>
    </div>
    
    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="p-2 bg-blue-100 rounded-lg">
            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">การประชุมทั้งหมด</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.totalMeetings }}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="p-2 bg-green-100 rounded-lg">
            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">วาระทั้งหมด</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.totalAgendas }}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="p-2 bg-yellow-100 rounded-lg">
            <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">วาระรอดำเนินการ</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.pendingAgendas }}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="p-2 bg-purple-100 rounded-lg">
            <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">รายงานทั้งหมด</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.totalReports }}</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Quick Actions -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold text-gray-800 mb-4">การประชุมล่าสุด</h2>
        <div class="space-y-4">
          <div v-for="meeting in recentMeetings" :key="meeting.id" class="border-l-4 border-blue-500 pl-4">
            <h3 class="font-medium text-gray-900">{{ meeting.name }}</h3>
            <p class="text-sm text-gray-600">{{ meeting.date }} | {{ meeting.status }}</p>
          </div>
        </div>
        <router-link to="/current-meeting" class="inline-block mt-4 text-blue-600 hover:text-blue-800">
          ดูวาระประชุมปัจจุบัน →
        </router-link>
      </div>
      
      <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold text-gray-800 mb-4">การดำเนินการด่วน</h2>
        <div class="space-y-3">
          <router-link 
            to="/current-meeting" 
            class="block w-full bg-blue-600 text-white text-center py-2 px-4 rounded hover:bg-blue-700"
          >
            ดูวาระประชุมปัจจุบัน
          </router-link>
          <router-link 
            to="/reports-history" 
            class="block w-full bg-green-600 text-white text-center py-2 px-4 rounded hover:bg-green-700"
          >
            ดูรายงานการประชุม
          </router-link>
          <router-link 
            to="/search-reports" 
            class="block w-full bg-purple-600 text-white text-center py-2 px-4 rounded hover:bg-purple-700"
          >
            ค้นหารายงาน
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'Dashboard',
  setup() {
    const stats = ref({
      totalMeetings: 0,
      totalAgendas: 0,
      pendingAgendas: 0,
      totalReports: 0
    })
    
    const recentMeetings = ref([])
    
    const loadDashboardData = async () => {
      // TODO: Load actual data from API
      // Mock data for now
      stats.value = {
        totalMeetings: 25,
        totalAgendas: 147,
        pendingAgendas: 8,
        totalReports: 23
      }
      
      recentMeetings.value = [
        { id: 1, name: 'ประชุมคณะกรรมการบริหาร ครั้งที่ 3/2567', date: '15 มี.ค. 2567', status: 'กำลังดำเนินการ' },
        { id: 2, name: 'ประชุมทบทวนคุณภาพ ครั้งที่ 2/2567', date: '10 มี.ค. 2567', status: 'เสร็จสิ้น' },
        { id: 3, name: 'ประชุมแผนกเทคโนโลยี ครั้งที่ 1/2567', date: '5 มี.ค. 2567', status: 'เสร็จสิ้น' }
      ]
    }
    
    onMounted(() => {
      loadDashboardData()
    })
    
    return {
      stats,
      recentMeetings
    }
  }
}
</script>