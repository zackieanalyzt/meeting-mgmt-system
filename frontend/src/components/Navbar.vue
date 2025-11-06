<template>
  <nav class="bg-blue-600 text-white shadow-lg fixed w-full top-0 z-50">
    <div class="container mx-auto px-4">
      <div class="flex justify-between items-center h-16">
        <div class="flex items-center space-x-8">
          <router-link to="/dashboard" class="text-xl font-bold hover:text-blue-200">
            ระบบจัดการการประชุม
          </router-link>
          
          <div class="hidden md:flex space-x-6">
            <router-link 
              to="/dashboard" 
              class="nav-link"
              :class="{ 'text-blue-200': $route.name === 'Dashboard' }"
            >
              แดชบอร์ด
            </router-link>
            <router-link 
              to="/current-meeting" 
              class="nav-link"
              :class="{ 'text-blue-200': $route.name === 'CurrentMeeting' }"
            >
              วาระประชุมปัจจุบัน
            </router-link>
            <router-link 
              to="/reports-history" 
              class="nav-link"
              :class="{ 'text-blue-200': $route.name === 'ReportsHistory' }"
            >
              รายงานการประชุม
            </router-link>
            <router-link 
              to="/search-reports" 
              class="nav-link"
              :class="{ 'text-blue-200': $route.name === 'SearchReports' }"
            >
              ค้นหารายงาน
            </router-link>
          </div>
        </div>
        
        <div class="flex items-center space-x-4">
          <span class="text-sm">{{ userInfo.fullname || 'ผู้ใช้' }}</span>
          <button 
            @click="logout" 
            class="bg-blue-700 hover:bg-blue-800 px-3 py-1 rounded text-sm"
          >
            ออกจากระบบ
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'Navbar',
  setup() {
    const router = useRouter()
    const userInfo = ref({
      fullname: 'ผู้ใช้ทดสอบ'
    })
    
    const logout = () => {
      localStorage.removeItem('token')
      router.push('/login')
    }
    
    return {
      userInfo,
      logout
    }
  }
}
</script>

<style scoped>
.nav-link {
  @apply hover:text-blue-200 transition-colors duration-200;
}
</style>