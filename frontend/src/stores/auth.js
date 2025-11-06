import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null,
    isAuthenticated: false
  }),
  
  actions: {
    async login(credentials) {
      // TODO: Implement login logic
    },
    
    async logout() {
      // TODO: Implement logout logic
    },
    
    async fetchUser() {
      // TODO: Fetch current user
    }
  }
})