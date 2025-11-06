<template>
  <div class="container mx-auto px-4 py-8">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-2">ค้นหารายงานการประชุม</h1>
      <p class="text-gray-600">ค้นหาข้อมูลจากรายงานการประชุมทั้งหมด</p>
    </div>
    
    <!-- Search Form -->
    <div class="bg-white rounded-lg shadow p-6 mb-8">
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            คำค้นหา
          </label>
          <div class="flex space-x-4">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="กรอกคำที่ต้องการค้นหา..."
              class="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              @keyup.enter="performSearch"
            />
            <button
              @click="performSearch"
              :disabled="!searchQuery.trim()"
              class="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              ค้นหา
            </button>
          </div>
        </div>
        
        <!-- Advanced Search Options -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">ช่วงวันที่</label>
            <div class="flex space-x-2">
              <input
                v-model="searchFilters.dateFrom"
                type="date"
                class="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <input
                v-model="searchFilters.dateTo"
                type="date"
                class="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">ประเภทการค้นหา</label>
            <select 
              v-model="searchFilters.searchType"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">ทั้งหมด</option>
              <option value="title">ชื่อการประชุม</option>
              <option value="agenda">วาระการประชุม</option>
              <option value="content">เนื้อหารายงาน</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">เรียงลำดับ</label>
            <select 
              v-model="searchFilters.sortBy"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="date_desc">วันที่ (ใหม่ → เก่า)</option>
              <option value="date_asc">วันที่ (เก่า → ใหม่)</option>
              <option value="relevance">ความเกี่ยวข้อง</option>
            </select>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Search Results -->
    <div v-if="hasSearched">
      <div class="mb-6">
        <p class="text-gray-600">
          พบ <span class="font-semibold">{{ searchResults.length }}</span> รายการ
          <span v-if="searchQuery">สำหรับ "<span class="font-semibold">{{ searchQuery }}</span>"</span>
          <span v-if="searchTime">({{ searchTime }} วินาที)</span>
        </p>
      </div>
      
      <div v-if="searchResults.length > 0" class="space-y-6">
        <div 
          v-for="result in searchResults" 
          :key="result.id"
          class="bg-white rounded-lg shadow hover:shadow-md transition-shadow p-6"
        >
          <div class="flex justify-between items-start mb-4">
            <div class="flex-1">
              <h3 class="text-xl font-semibold text-gray-800 mb-2">
                <span v-html="highlightText(result.meetingName)"></span>
              </h3>
              <p class="text-gray-600 mb-2">{{ result.date }} | {{ result.location }}</p>
              
              <!-- Search Highlights -->
              <div class="space-y-2">
                <div v-for="highlight in result.highlights" :key="highlight.id" class="text-sm">
                  <span class="font-medium text-gray-700">{{ highlight.type }}:</span>
                  <span v-html="highlightText(highlight.text)" class="text-gray-600 ml-2"></span>
                </div>
              </div>
            </div>
            
            <div class="flex items-center space-x-3 ml-4">
              <span class="text-sm text-gray-500">
                คะแนน: {{ result.relevanceScore }}%
              </span>
              <button 
                @click="viewResult(result)"
                class="text-blue-600 hover:text-blue-800 text-sm font-medium"
              >
                ดูรายงาน
              </button>
            </div>
          </div>
          
          <!-- Tags -->
          <div class="flex flex-wrap gap-2">
            <span 
              v-for="tag in result.tags" 
              :key="tag"
              class="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs"
            >
              {{ tag }}
            </span>
          </div>
        </div>
      </div>
      
      <div v-else class="text-center py-12">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">ไม่พบผลการค้นหา</h3>
        <p class="mt-1 text-sm text-gray-500">ลองใช้คำค้นหาอื่น หรือปรับเปลี่ยนตัวกรอง</p>
      </div>
    </div>
    
    <!-- Recent Searches -->
    <div v-if="!hasSearched && recentSearches.length > 0" class="bg-white rounded-lg shadow p-6">
      <h2 class="text-lg font-semibold text-gray-800 mb-4">การค้นหาล่าสุด</h2>
      <div class="space-y-2">
        <button
          v-for="search in recentSearches"
          :key="search.id"
          @click="loadRecentSearch(search)"
          class="block w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded"
        >
          <span class="font-medium">{{ search.query }}</span>
          <span class="text-gray-500 ml-2">{{ search.date }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'SearchReports',
  setup() {
    const searchQuery = ref('')
    const searchResults = ref([])
    const hasSearched = ref(false)
    const searchTime = ref(null)
    const recentSearches = ref([])
    
    const searchFilters = ref({
      dateFrom: '',
      dateTo: '',
      searchType: 'all',
      sortBy: 'date_desc'
    })
    
    const performSearch = async () => {
      if (!searchQuery.value.trim()) return
      
      const startTime = Date.now()
      hasSearched.value = true
      
      // TODO: Implement actual search API call
      // Mock search results
      await new Promise(resolve => setTimeout(resolve, 500))
      
      searchResults.value = [
        {
          id: 1,
          meetingName: 'ประชุมคณะกรรมการบริหาร ครั้งที่ 2/2567',
          date: '10 มีนาคม 2567',
          location: 'ห้องประชุมใหญ่',
          relevanceScore: 95,
          highlights: [
            { id: 1, type: 'วาระ', text: 'พิจารณาแผนงานประจำเดือน และติดตามผลการดำเนินงาน' },
            { id: 2, type: 'เนื้อหา', text: 'การประเมินผลการดำเนินงานในไตรมาสที่ผ่านมา' }
          ],
          tags: ['แผนงาน', 'การประเมิน', 'ไตรมาส']
        },
        {
          id: 2,
          meetingName: 'ประชุมทบทวนคุณภาพ ครั้งที่ 1/2567',
          date: '5 มีนาคม 2567',
          location: 'ห้องประชุมเล็ก',
          relevanceScore: 78,
          highlights: [
            { id: 3, type: 'วาระ', text: 'ทบทวนระบบคุณภาพและการปรับปรุงกระบวนการ' }
          ],
          tags: ['คุณภาพ', 'ปรับปรุง', 'กระบวนการ']
        }
      ]
      
      const endTime = Date.now()
      searchTime.value = ((endTime - startTime) / 1000).toFixed(2)
      
      // Save to recent searches
      saveRecentSearch(searchQuery.value)
    }
    
    const highlightText = (text) => {
      if (!searchQuery.value.trim()) return text
      const regex = new RegExp(`(${searchQuery.value})`, 'gi')
      return text.replace(regex, '<mark class="bg-yellow-200">$1</mark>')
    }
    
    const viewResult = (result) => {
      // TODO: Navigate to report detail
      console.log('View result:', result.id)
    }
    
    const saveRecentSearch = (query) => {
      const newSearch = {
        id: Date.now(),
        query,
        date: new Date().toLocaleDateString('th-TH')
      }
      
      recentSearches.value.unshift(newSearch)
      recentSearches.value = recentSearches.value.slice(0, 5) // Keep only 5 recent searches
    }
    
    const loadRecentSearch = (search) => {
      searchQuery.value = search.query
      performSearch()
    }
    
    const loadRecentSearches = () => {
      // TODO: Load from localStorage or API
      recentSearches.value = [
        { id: 1, query: 'แผนงานประจำเดือน', date: '14 มี.ค. 2567' },
        { id: 2, query: 'คุณภาพ', date: '13 มี.ค. 2567' }
      ]
    }
    
    onMounted(() => {
      loadRecentSearches()
    })
    
    return {
      searchQuery,
      searchResults,
      searchFilters,
      hasSearched,
      searchTime,
      recentSearches,
      performSearch,
      highlightText,
      viewResult,
      loadRecentSearch
    }
  }
}
</script>