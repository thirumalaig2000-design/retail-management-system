import api from './api'

export const supplierService = {
  list: async (params = {}) => (await api.get('/suppliers/', { params })).data,
  create: async (payload) => (await api.post('/suppliers/', payload)).data,
  update: async (id, payload) => (await api.patch(`/suppliers/${id}/`, payload)).data,
  remove: async (id) => (await api.delete(`/suppliers/${id}/`)).data,
}
