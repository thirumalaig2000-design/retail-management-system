import api from './api'

export const salesService = {
  list: async (params = {}) => (await api.get('/sales/', { params })).data,
  create: async (payload) => (await api.post('/sales/', payload)).data,
  complete: async (id, payload) => (await api.post(`/sales/${id}/complete/`, payload)).data,
}
