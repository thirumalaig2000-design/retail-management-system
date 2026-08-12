import api from './api'

export const inventoryService = {
  list: async (params = {}) => (await api.get('/inventory/', { params })).data,
  transactions: async (params = {}) => (await api.get('/inventory/transactions/', { params })).data,
  adjust: async (payload) => (await api.post('/inventory/adjust/', payload)).data,
}
