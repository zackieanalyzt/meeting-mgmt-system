<template>
  <div class="container mx-auto px-4 py-8">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-2">วาระการประชุมปัจจุบัน</h1>
      <p class="text-gray-600">ดูและจัดการวาระการประชุมที่กำลังดำเนินการ</p>
    </div>
    
    <!-- Current Meeting Info -->
    <div class="bg-white rounded-lg shadow mb-8 p-6">
      <div class="flex justify-between items-start mb-4">
        <div>
          <h2 class="text-xl font-semibold text-gray-800">{{ currentMeeting.name }}</h2>
          <p class="text-gray-600">{{ currentMeeting.date }} | {{ currentMeeting.time }} | {{ currentMeeting.location }}</p>
        </div>
        <span class="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
          {{ currentMeeting.status }}
        </span>
      </div>
      <p class="text-gray-700">{{ currentMeeting.description }}</p>
    </div>
    
    <!-- Add Agenda Button -->
    <div class="mb-6">
      <button 
        @click="showAddAgenda = true"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        + เพิ่มวาระใหม่
      </button>
    </div>
    
    <!-- Agendas List -->
    <div class="space-y-4">
      <div 
        v-for="agenda in agendas" 
        :key="agenda.id"
        class="bg-white rounded-lg shadow p-6"
      >
        <div class="flex justify-between items-start mb-4">
          <div class="flex-1">
            <div class="flex items-center mb-2">
              <span class="text-sm font-medium text-gray-500 mr-2">วาระที่ {{ agenda.order }}</span>
              <span 
                class="px-2 py-1 text-xs rounded-full"
                :class="getAgendaTypeClass(agenda.type)"
              >
                {{ agenda.type }}
              </span>
            </div>
            <h3 class="text-lg font-semibold text-gray-800 mb-2">{{ agenda.title }}</h3>
            <p class="text-gray-600 mb-4">{{ agenda.detail }}</p>
            
            <!-- Files -->
            <div v-if="agenda.files.length > 0" class="mb-4">
              <h4 class="text-sm font-medium text-gray-700 mb-2">ไฟล์แนบ:</h4>
              <div class="flex flex-wrap gap-2">
                <span 
                  v-for="file in agenda.files" 
                  :key="file.id"
                  class="inline-flex items-center px-3 py-1 bg-gray-100 text-gray-700 rounded text-sm"
                >
                  📎 {{ file.name }}
                </span>
              </div>
            </div>
          </div>
          
          <div class="flex space-x-2 ml-4">
            <button class="text-blue-600 hover:text-blue-800 text-sm">แก้ไข</button>
            <button class="text-red-600 hover:text-red-800 text-sm">ลบ</button>
          </div>
        </div>
        
        <div class="text-sm text-gray-500">
          เสนอโดย: {{ agenda.createdBy }} | {{ agenda.createdAt }}
        </div>
      </div>
    </div>
    
    <!-- Add Agenda Modal Placeholder -->
    <div v-if="showAddAgenda" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h3 class="text-lg font-semibold mb-4">เพิ่มวาระใหม่</h3>
        <p class="text-gray-600 mb-4">ฟอร์มเพิ่มวาระจะอยู่ที่นี่</p>
        <button 
          @click="showAddAgenda = false"
          class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
        >
          ปิด
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'CurrentMeeting',
  setup() {
    const showAddAgenda = ref(false)
    const currentMeeting = ref({})
    const agendas = ref([])
    
    const getAgendaTypeClass = (type) => {
      const classes = {
        'เพื่อทราบ': 'bg-blue-100 text-blue-800',
        'เพื่อพิจารณา': 'bg-yellow-100 text-yellow-800',
        'เพื่อสั่งการ': 'bg-red-100 text-red-800'
      }
      return classes[type] || 'bg-gray-100 text-gray-800'
    }
    
    const loadCurrentMeeting = async () => {
      // TODO: Load from API
      currentMeeting.value = {
        id: 1,
        name: 'ประชุมคณะกรรมการบริหาร ครั้งที่ 3/2567',
        date: '15 มีนาคม 2567',
        time: '09:00 น.',
        location: 'ห้องประชุมใหญ่',
        status: 'กำลังดำเนินการ',
        description: 'ประชุมเพื่อพิจารณาแผนงานประจำเดือนและติดตามผลการดำเนินงาน'
      }
      
      agendas.value = [
        {
          id: 1,
          order: 1,
          title: 'รับรองรายงานการประชุมครั้งที่แล้ว',
          detail: 'พิจารณารับรองรายงานการประชุมคณะกรรมการบริหาร ครั้งที่ 2/2567',
          type: 'เพื่อพิจารณา',
          files: [{ id: 1, name: 'รายงานการประชุม_ครั้งที่2.pdf' }],
          createdBy: 'นายสมชาย ใจดี',
          createdAt: '10 มี.ค. 2567'
        },
        {
          id: 2,
          order: 2,
          title: 'รายงานผลการดำเนินงานประจำเดือน',
          detail: 'รายงานสรุปผลการดำเนินงานของแต่ละแผนกในเดือนที่ผ่านมา',
          type: 'เพื่อทราบ',
          files: [],
          createdBy: 'นางสาวมาลี สวยงาม',
          createdAt: '12 มี.ค. 2567'
        }
      ]
    }
    
    onMounted(() => {
      loadCurrentMeeting()
    })
    
    return {
      showAddAgenda,
      currentMeeting,
      agendas,
      getAgendaTypeClass
    }
  }
}
</script>