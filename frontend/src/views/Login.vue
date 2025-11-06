<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100 flex items-center justify-center">
    <div class="bg-white p-8 rounded-xl shadow-lg w-full max-w-md">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-800 mb-2">ระบบจัดการการประชุม</h1>
        <p class="text-gray-600">โรงพยาบาลลี้ - กลุ่มงานสุขภาพดิจิทัล</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            ชื่อผู้ใช้
          </label>
          <input
            v-model="loginForm.username"
            type="text"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="กรอกชื่อผู้ใช้"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            รหัสผ่าน
          </label>
          <input
            v-model="loginForm.password"
            type="password"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="กรอกรหัสผ่าน"
          />
        </div>
        
        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
        >
          {{ loading ? 'กำลังเข้าสู่ระบบ...' : 'เข้าสู่ระบบ' }}
        </button>
      </form>
      
      <div v-if="error" class="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const loading = ref(false)
    const error = ref('')
    
    const loginForm = ref({
      username: '',
      password: ''
    })
    
    const handleLogin = async () => {
      loading.value = true
      error.value = ''
      
      try {
        // TODO: Implement actual login API call
        // Simulate login for now
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        // Mock successful login
        localStorage.setItem('token', 'mock-jwt-token')
        router.push('/dashboard')
      } catch (err) {
        error.value = 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง'
      } finally {
        loading.value = false
      }
    }
    
    return {
      loginForm,
      loading,
      error,
      handleLogin
    }
  }
}
</script>