import api from './api'

export const productService = {
  list: async (params = {}) => (await api.get('/products/', { params })).data,
  create: async (payload) => (await api.post('/products/', payload)).data,
  update: async (id, payload) => (await api.patch(`/products/${id}/`, payload)).data,
  remove: async (id) => (await api.delete(`/products/${id}/`)).data,
  activate: async (id) => (await api.post(`/products/${id}/activate/`)).data,
  deactivate: async (id) => (await api.post(`/products/${id}/deactivate/`)).data,
}
