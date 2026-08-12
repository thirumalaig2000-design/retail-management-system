import api from './api'
import { storage } from './storage'

export async function login(email, password) {
  const { data } = await api.post('/auth/login/', { email, password })
  storage.setSession(data)
  return data
}

export async function fetchProfile() {
  const { data } = await api.get('/auth/me/')
  return data
}

export async function logout() {
  const refresh = storage.getRefreshToken()
  if (refresh) {
    await api.post('/auth/logout/', { refresh })
  }
  storage.clearSession()
}
