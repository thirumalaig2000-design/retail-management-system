import axios from 'axios'
import { storage } from './storage'

const baseURL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, '') || 'http://localhost:8000/api'

const api = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use((config) => {
  const token = storage.getAccessToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

let refreshPromise = null

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    if (
      error.response?.status === 401 &&
      originalRequest &&
      !originalRequest._retry &&
      storage.getRefreshToken()
    ) {
      originalRequest._retry = true
      try {
        refreshPromise =
          refreshPromise ||
          axios.post(`${baseURL}/auth/refresh/`, {
            refresh: storage.getRefreshToken(),
          })

        const refreshResponse = await refreshPromise
        refreshPromise = null
        const newAccess = refreshResponse.data.access
        const sessionUser = storage.getUser()
        storage.setSession({
          access: newAccess,
          refresh: storage.getRefreshToken(),
          user: sessionUser,
        })
        originalRequest.headers.Authorization = `Bearer ${newAccess}`
        return api(originalRequest)
      } catch (refreshError) {
        refreshPromise = null
        storage.clearSession()
        window.dispatchEvent(new Event('smartstock:auth-expired'))
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  },
)

export default api
