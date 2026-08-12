import api from './api'

export const invoiceService = {
  list: async (params = {}) => (await api.get('/invoices/', { params })).data,
}
