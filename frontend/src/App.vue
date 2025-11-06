<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <Navbar v-if="showNavbar" />
    <main :class="showNavbar ? 'pt-16' : ''">
      <router-view />
    </main>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Navbar from './components/Navbar.vue'

export default {
  name: 'App',
  components: {
    Navbar
  },
  setup() {
    const route = useRoute()
    
    const showNavbar = computed(() => {
      return route.name !== 'Login'
    })
    
    return {
      showNavbar
    }
  }
}
</script>