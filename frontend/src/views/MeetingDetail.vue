<template>
  <div class="container mx-auto px-4 py-8 max-w-4xl">
    <div v-if="isLoading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      <p class="mt-4 text-gray-600">กำลังโหลดข้อมูล...</p>
    </div>

    <div v-else-if="errorMessage" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
      <p class="font-medium">เกิดข้อผิดพลาด</p>
      <p class="text-sm">{{ errorMessage }}</p>
      <button @click="$router.push('/meetings')" class="mt-2 text-sm underline">กลับไปหน้ารายการ</button>
    </div>

    <div v-else-if="meeting" class="bg-white rounded-lg shadow-md p-6">
      <div class="mb-6">
        <button @click="$router.push('/meetings')" class="text-blue-600 hover:text-blue-800 mb-4">
          ← กลับไปหน้ารายการ
        </button>
        <div class="flex justify-between items-start">
          <h1 class="text-3xl font-bold text-gray-800">{{ meeting.meeting_title }}</h1>
          <span :class="['px-3 py-1 rounded-full text-sm font-semibold', meeting.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800']">
            {{ meeting.status === 'active' ? 'กำลังดำเนินการ' : 'ปิดแล้ว' }}
          </span>
        </div>
      </div>

      <div class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <div><strong>วันที่:</strong> {{ formatDate(meeting.meeting_date) }}</div>
          <div><strong>เวลา:</strong> {{ formatTime(meeting.start_time) }} - {{ formatTime(meeting.end_time) }}</div>
          <div><strong>สถานที่:</strong> {{ meeting.location }}</div>
          <div v-if="meeting.created_by_fullname"><strong>สร้างโดย:</strong> {{ meeting.created_by_fullname }}</div>
        </div>
        <div v-if="meeting.description">
          <strong>รายละเอียด:</strong>
          <p class="mt-2 text-gray-700">{{ meeting.description }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api'

export default {
  name: 'MeetingDetail',
  setup() {
    const route = useRoute()
    const meeting = ref(null)
    const isLoading = ref(false)
    const errorMessage = ref('')
    
    const fetchMeeting = async () => {
      isLoading.value = true
      try {
        const response = await api.get(`/meetings/${route.params.id}`)
        meeting.value = response.data
      } catch (error) {
        errorMessage.value = 'ไม่สามารถโหลดข้อมูลได้'
      } finally {
        isLoading.value = false
      }
    }
    
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('th-TH', { year: 'numeric', month: 'long', day: 'numeric' })
    }
    
    const formatTime = (timeString) => timeString ? timeString.substring(0, 5) : ''
    
    onMounted(fetchMeeting)
    
    return { meeting, isLoading, errorMessage, formatDate, formatTime }
  }
}
</script>
