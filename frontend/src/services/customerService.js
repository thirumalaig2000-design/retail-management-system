import api from './api'

export const customerService = {
  list: async (params = {}) => (await api.get('/customers/', { params })).data,
  create: async (payload) => (await api.post('/customers/', payload)).data,
  update: async (id, payload) => (await api.patch(`/customers/${id}/`, payload)).data,
  remove: async (id) => (await api.delete(`/customers/${id}/`)).data,
}
