import api from './api'

export const categoryService = {
  list: async (params = {}) => (await api.get('/categories/', { params })).data,
  create: async (payload) => (await api.post('/categories/', payload)).data,
  update: async (id, payload) => (await api.patch(`/categories/${id}/`, payload)).data,
  remove: async (id) => (await api.delete(`/categories/${id}/`)).data,
  activate: async (id) => (await api.post(`/categories/${id}/activate/`)).data,
  deactivate: async (id) => (await api.post(`/categories/${id}/deactivate/`)).data,
}
