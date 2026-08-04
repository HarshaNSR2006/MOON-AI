import axios from 'axios'

const configuredBase = (import.meta.env.VITE_API_BASE as string | undefined)?.trim() || '/api'

const api = axios.create({
  baseURL: configuredBase,
  timeout: 15000,
})

// Attach token from localStorage if present
api.interceptors.request.use((config) => {
  try {
    const token = localStorage.getItem('moon_token')
    if (token && config.headers) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
  } catch (e) {
    // ignore
  }
  return config
})

export default api
