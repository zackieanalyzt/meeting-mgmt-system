<template>
  <div class="container mx-auto px-4 py-8 max-w-4xl">
    <div class="bg-white rounded-lg shadow-md p-6">
      <div class="mb-6">
        <h1 class="text-3xl font-bold text-gray-800">สร้างการประชุมใหม่</h1>
        <p class="text-gray-600 mt-2">กรอกข้อมูลการประชุมที่ต้องการสร้าง</p>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Meeting Title -->
        <div>
          <label for="meeting_title" class="block text-sm font-medium text-gray-700 mb-2">
            ชื่อการประชุม <span class="text-red-500">*</span>
          </label>
          <input
            id="meeting_title"
            v-model="formData.meeting_title"
            type="text"
            required
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="เช่น ประชุมคณะกรรมการบริหาร ครั้งที่ 1/2567"
          />
        </div>

        <!-- Meeting Date and Times -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label for="meeting_date" class="block text-sm font-medium text-gray-700 mb-2">
              วันที่ประชุม <span class="text-red-500">*</span>
            </label>
            <input
              id="meeting_date"
              v-model="formData.meeting_date"
              type="date"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div>
            <label for="start_time" class="block text-sm font-medium text-gray-700 mb-2">
              เวลาเริ่ม <span class="text-red-500">*</span>
            </label>
            <input
              id="start_time"
              v-model="formData.start_time"
              type="time"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div>
            <label for="end_time" class="block text-sm font-medium text-gray-700 mb-2">
              เวลาสิ้นสุด <span class="text-red-500">*</span>
            </label>
            <input
              id="end_time"
              v-model="formData.end_time"
              type="time"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>

        <!-- Location -->
        <div>
          <label for="location" class="block text-sm font-medium text-gray-700 mb-2">
            สถานที่ <span class="text-red-500">*</span>
          </label>
          <input
            id="location"
            v-model="formData.location"
            type="text"
            required
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="เช่น ห้องประชุม 1 ชั้น 3"
          />
        </div>

        <!-- Description -->
        <div>
          <label for="description" class="block text-sm font-medium text-gray-700 mb-2">
            รายละเอียด
          </label>
          <textarea
            id="description"
            v-model="formData.description"
            rows="4"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="รายละเอียดเพิ่มเติมเกี่ยวกับการประชุม..."
          ></textarea>
        </div>

        <!-- Error Message -->
        <div v-if="errorMessage" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          <p class="font-medium">เกิดข้อผิดพลาด</p>
          <p class="text-sm">{{ errorMessage }}</p>
        </div>

        <!-- Success Message -->
        <div v-if="successMessage" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg">
          <p class="font-medium">สำเร็จ!</p>
          <p class="text-sm">{{ successMessage }}</p>
        </div>

        <!-- Action Buttons -->
        <div class="flex justify-end space-x-4 pt-4">
          <button
            type="button"
            @click="handleCancel"
            class="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
            :disabled="isSubmitting"
          >
            ยกเลิก
          </button>
          <button
            type="submit"
            class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
            :disabled="isSubmitting"
          >
            <span v-if="isSubmitting">กำลังบันทึก...</span>
            <span v-else>สร้างการประชุม</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

export default {
  name: 'MeetingCreate',
  setup() {
    const router = useRouter()
    
    const formData = ref({
      meeting_title: '',
      meeting_date: '',
      start_time: '',
      end_time: '',
      location: '',
      description: ''
    })
    
    const isSubmitting = ref(false)
    const errorMessage = ref('')
    const successMessage = ref('')
    
    const validateForm = () => {
      // Check if end_time is after start_time
      if (formData.value.start_time && formData.value.end_time) {
        if (formData.value.end_time <= formData.value.start_time) {
          errorMessage.value = 'เวลาสิ้นสุดต้องมากกว่าเวลาเริ่มต้น'
          return false
        }
      }
      return true
    }
    
    const handleSubmit = async () => {
      errorMessage.value = ''
      successMessage.value = ''
      
      if (!validateForm()) {
        return
      }
      
      isSubmitting.value = true
      
      try {
        const response = await api.post('/meetings', formData.value)
        
        successMessage.value = 'สร้างการประชุมสำเร็จ กำลังนำคุณไปยังหน้ารายการการประชุม...'
        
        // Redirect after 1.5 seconds
        setTimeout(() => {
          router.push('/meetings')
        }, 1500)
        
      } catch (error) {
        console.error('Error creating meeting:', error)
        
        if (error.response?.data?.detail) {
          errorMessage.value = error.response.data.detail
        } else if (error.response?.status === 403) {
          errorMessage.value = 'คุณไม่มีสิทธิ์ในการสร้างการประชุม'
        } else if (error.response?.status === 401) {
          errorMessage.value = 'กรุณาเข้าสู่ระบบใหม่อีกครั้ง'
          setTimeout(() => {
            router.push('/login')
          }, 2000)
        } else {
          errorMessage.value = 'ไม่สามารถสร้างการประชุมได้ กรุณาลองใหม่อีกครั้ง'
        }
      } finally {
        isSubmitting.value = false
      }
    }
    
    const handleCancel = () => {
      if (confirm('คุณต้องการยกเลิกการสร้างการประชุมหรือไม่?')) {
        router.push('/meetings')
      }
    }
    
    return {
      formData,
      isSubmitting,
      errorMessage,
      successMessage,
      handleSubmit,
      handleCancel
    }
  }
}
</script>

<style scoped>
/* Additional custom styles if needed */
</style>
