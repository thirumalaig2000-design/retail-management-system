import api from './api'

export const getDashboard = () => api.get('/dashboard/').then((response) => response.data)
export const getReport = (name, params = {}) => api.get(`/reports/${name}/`, { params }).then((response) => response.data)
