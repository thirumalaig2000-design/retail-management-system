import api from './api'

export const purchaseService = {
  list: async (params = {}) => (await api.get('/purchases/', { params })).data,
  create: async (payload) => (await api.post('/purchases/', payload)).data,
  receive: async (id, payload = {}) => (await api.post(`/purchases/${id}/receive/`, payload)).data,
}
