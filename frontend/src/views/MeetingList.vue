<template>
  <div class="container mx-auto px-4 py-8">
    <div class="mb-6 flex justify-between items-center">
      <div>
        <h1 class="text-3xl font-bold text-gray-800">รายการการประชุม</h1>
        <p class="text-gray-600 mt-2">จัดการและดูรายการการประชุมทั้งหมด</p>
      </div>
      <router-link
        to="/meetings/create"
        class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg transition-colors flex items-center space-x-2"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        <span>สร้างการประชุมใหม่</span>
      </router-link>
    </div>

    <!-- Filter Section -->
    <div class="bg-white rounded-lg shadow-md p-4 mb-6">
      <div class="flex items-center space-x-4">
        <label class="text-sm font-medium text-gray-700">กรองตามสถานะ:</label>
        <select
          v-model="filterStatus"
          @change="fetchMeetings"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="all">ทั้งหมด ({{ totalCount }})</option>
          <option value="active">กำลังดำเนินการ ({{ activeCount }})</option>
          <option value="closed">ปิดแล้ว ({{ closedCount }})</option>
        </select>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      <p class="mt-4 text-gray-600">กำลังโหลดข้อมูล...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="errorMessage" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
      <p class="font-medium">เกิดข้อผิดพลาด</p>
      <p class="text-sm">{{ errorMessage }}</p>
      <button @click="fetchMeetings" class="mt-2 text-sm underline">ลองใหม่อีกครั้ง</button>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredMeetings.length === 0" class="bg-white rounded-lg shadow-md p-12 text-center">
      <svg class="mx-auto h-16 w-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
      </svg>
      <h3 class="mt-4 text-lg font-medium text-gray-900">ไม่พบการประชุม</h3>
      <p class="mt-2 text-gray-600">ยังไม่มีการประชุมในระบบ</p>
      <router-link
        to="/meetings/create"
        class="mt-4 inline-block bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition-colors"
      >
        สร้างการประชุมแรก
      </router-link>
    </div>

    <!-- Meetings Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="meeting in filteredMeetings"
        :key="meeting.meeting_id"
        class="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow cursor-pointer overflow-hidden"
        @click="viewMeeting(meeting.meeting_id)"
      >
        <div class="p-6">
          <!-- Status Badge -->
          <div class="flex justify-between items-start mb-3">
            <span
              :class="[
                'px-3 py-1 rounded-full text-xs font-semibold',
                meeting.status === 'active' 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-gray-100 text-gray-800'
              ]"
            >
              {{ meeting.status === 'active' ? 'กำลังดำเนินการ' : 'ปิดแล้ว' }}
            </span>
          </div>

          <!-- Meeting Title -->
          <h3 class="text-lg font-bold text-gray-800 mb-2 line-clamp-2">
            {{ meeting.meeting_title }}
          </h3>

          <!-- Meeting Info -->
          <div class="space-y-2 text-sm text-gray-600">
            <div class="flex items-center">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <span>{{ formatDate(meeting.meeting_date) }}</span>
            </div>

            <div class="flex items-center">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>{{ formatTime(meeting.start_time) }} - {{ formatTime(meeting.end_time) }}</span>
            </div>

            <div class="flex items-center">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <span>{{ meeting.location }}</span>
            </div>

            <div v-if="meeting.created_by_fullname" class="flex items-center">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              <span>สร้างโดย: {{ meeting.created_by_fullname }}</span>
            </div>
          </div>

          <!-- Description Preview -->
          <p v-if="meeting.description" class="mt-3 text-sm text-gray-600 line-clamp-2">
            {{ meeting.description }}
          </p>
        </div>

        <!-- Card Footer -->
        <div class="bg-gray-50 px-6 py-3 border-t border-gray-200">
          <button
            @click.stop="viewMeeting(meeting.meeting_id)"
            class="text-blue-600 hover:text-blue-800 text-sm font-medium"
          >
            ดูรายละเอียด →
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

export default {
  name: 'MeetingList',
  setup() {
    const router = useRouter()
    
    const meetings = ref([])
    const isLoading = ref(false)
    const errorMessage = ref('')
    const filterStatus = ref('all')
    
    const filteredMeetings = computed(() => {
      if (filterStatus.value === 'all') {
        return meetings.value
      }
      return meetings.value.filter(m => m.status === filterStatus.value)
    })
    
    const totalCount = computed(() => meetings.value.length)
    const activeCount = computed(() => meetings.value.filter(m => m.status === 'active').length)
    const closedCount = computed(() => meetings.value.filter(m => m.status === 'closed').length)
    
    const fetchMeetings = async () => {
      isLoading.value = true
      errorMessage.value = ''
      
      try {
        const response = await api.get('/meetings', {
          params: {
            skip: 0,
            limit: 100
          }
        })
        
        meetings.value = response.data
      } catch (error) {
        console.error('Error fetching meetings:', error)
        
        if (error.response?.status === 401) {
          errorMessage.value = 'กรุณาเข้าสู่ระบบใหม่อีกครั้ง'
          setTimeout(() => {
            router.push('/login')
          }, 2000)
        } else {
          errorMessage.value = 'ไม่สามารถโหลดข้อมูลการประชุมได้ กรุณาลองใหม่อีกครั้ง'
        }
      } finally {
        isLoading.value = false
      }
    }
    
    const viewMeeting = (meetingId) => {
      router.push(`/meetings/${meetingId}`)
    }
    
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('th-TH', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
    
    const formatTime = (timeString) => {
      if (!timeString) return ''
      return timeString.substring(0, 5) // HH:MM
    }
    
    onMounted(() => {
      fetchMeetings()
    })
    
    return {
      meetings,
      filteredMeetings,
      isLoading,
      errorMessage,
      filterStatus,
      totalCount,
      activeCount,
      closedCount,
      fetchMeetings,
      viewMeeting,
      formatDate,
      formatTime
    }
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
