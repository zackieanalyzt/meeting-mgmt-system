<template>
  <div class="container mx-auto px-4 py-8">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-2">รายงานการประชุม</h1>
      <p class="text-gray-600">ดูรายงานการประชุมย้อนหลังทั้งหมด</p>
    </div>
    
    <!-- Filters -->
    <div class="bg-white rounded-lg shadow p-6 mb-8">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">ปี</label>
          <select 
            v-model="filters.year" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">ทั้งหมด</option>
            <option value="2567">2567</option>
            <option value="2566">2566</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">เดือน</label>
          <select 
            v-model="filters.month" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">ทั้งหมด</option>
            <option value="1">มกราคม</option>
            <option value="2">กุมภาพันธ์</option>
            <option value="3">มีนาคม</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">สถานะ</label>
          <select 
            v-model="filters.status" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">ทั้งหมด</option>
            <option value="published">เผยแพร่แล้ว</option>
            <option value="draft">ร่าง</option>
          </select>
        </div>
      </div>
    </div>
    
    <!-- Reports List -->
    <div class="space-y-6">
      <div 
        v-for="report in filteredReports" 
        :key="report.id"
        class="bg-white rounded-lg shadow hover:shadow-md transition-shadow"
      >
        <div class="p-6">
          <div class="flex justify-between items-start mb-4">
            <div class="flex-1">
              <h3 class="text-xl font-semibold text-gray-800 mb-2">{{ report.meetingName }}</h3>
              <p class="text-gray-600 mb-2">{{ report.date }} | {{ report.location }}</p>
              <p class="text-gray-700">{{ report.summary }}</p>
            </div>
            
            <div class="flex items-center space-x-3 ml-4">
              <span 
                class="px-3 py-1 rounded-full text-sm font-medium"
                :class="getStatusClass(report.status)"
              >
                {{ getStatusText(report.status) }}
              </span>
              
              <div class="flex space-x-2">
                <button 
                  @click="viewReport(report)"
                  class="text-blue-600 hover:text-blue-800 text-sm font-medium"
                >
                  ดูรายงาน
                </button>
                <button 
                  v-if="report.fileUrl"
                  @click="downloadReport(report)"
                  class="text-green-600 hover:text-green-800 text-sm font-medium"
                >
                  ดาวน์โหลด
                </button>
              </div>
            </div>
          </div>
          
          <!-- Meeting Stats -->
          <div class="grid grid-cols-3 gap-4 pt-4 border-t border-gray-200">
            <div class="text-center">
              <p class="text-2xl font-semibold text-blue-600">{{ report.totalAgendas }}</p>
              <p class="text-sm text-gray-600">วาระทั้งหมด</p>
            </div>
            <div class="text-center">
              <p class="text-2xl font-semibold text-green-600">{{ report.attendees }}</p>
              <p class="text-sm text-gray-600">ผู้เข้าร่วม</p>
            </div>
            <div class="text-center">
              <p class="text-2xl font-semibold text-purple-600">{{ report.attachments }}</p>
              <p class="text-sm text-gray-600">ไฟล์แนบ</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Pagination -->
    <div class="mt-8 flex justify-center">
      <div class="flex space-x-2">
        <button 
          v-for="page in totalPages" 
          :key="page"
          @click="currentPage = page"
          class="px-3 py-2 rounded"
          :class="currentPage === page ? 'bg-blue-600 text-white' : 'bg-white text-gray-700 hover:bg-gray-50'"
        >
          {{ page }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'

export default {
  name: 'ReportsHistory',
  setup() {
    const reports = ref([])
    const currentPage = ref(1)
    const itemsPerPage = 10
    
    const filters = ref({
      year: '',
      month: '',
      status: ''
    })
    
    const filteredReports = computed(() => {
      let filtered = reports.value
      
      if (filters.value.year) {
        filtered = filtered.filter(report => report.year === filters.value.year)
      }
      
      if (filters.value.month) {
        filtered = filtered.filter(report => report.month === filters.value.month)
      }
      
      if (filters.value.status) {
        filtered = filtered.filter(report => report.status === filters.value.status)
      }
      
      return filtered
    })
    
    const totalPages = computed(() => {
      return Math.ceil(filteredReports.value.length / itemsPerPage)
    })
    
    const getStatusClass = (status) => {
      return status === 'published' 
        ? 'bg-green-100 text-green-800' 
        : 'bg-yellow-100 text-yellow-800'
    }
    
    const getStatusText = (status) => {
      return status === 'published' ? 'เผยแพร่แล้ว' : 'ร่าง'
    }
    
    const viewReport = (report) => {
      // TODO: Navigate to report detail
      console.log('View report:', report.id)
    }
    
    const downloadReport = (report) => {
      // TODO: Download report file
      console.log('Download report:', report.id)
    }
    
    const loadReports = async () => {
      // TODO: Load from API
      reports.value = [
        {
          id: 1,
          meetingName: 'ประชุมคณะกรรมการบริหาร ครั้งที่ 2/2567',
          date: '10 มีนาคม 2567',
          location: 'ห้องประชุมใหญ่',
          summary: 'ประชุมเพื่อพิจารณาแผนงานประจำเดือนและติดตามผลการดำเนินงาน',
          status: 'published',
          totalAgendas: 5,
          attendees: 12,
          attachments: 8,
          year: '2567',
          month: '3',
          fileUrl: '/reports/meeting-2-2567.pdf'
        },
        {
          id: 2,
          meetingName: 'ประชุมทบทวนคุณภาพ ครั้งที่ 1/2567',
          date: '5 มีนาคม 2567',
          location: 'ห้องประชุมเล็ก',
          summary: 'ประชุมทบทวนระบบคุณภาพและการปรับปรุงกระบวนการ',
          status: 'published',
          totalAgendas: 3,
          attendees: 8,
          attachments: 4,
          year: '2567',
          month: '3',
          fileUrl: '/reports/quality-review-1-2567.pdf'
        }
      ]
    }
    
    onMounted(() => {
      loadReports()
    })
    
    return {
      reports,
      filteredReports,
      filters,
      currentPage,
      totalPages,
      getStatusClass,
      getStatusText,
      viewReport,
      downloadReport
    }
  }
}
</script>