import api from './api'

export const getSystemSettings = () => api.get('/settings/').then((response) => response.data)

export const updateSystemSetting = (id, value) =>
  api.patch(`/settings/${id}/`, { value }).then((response) => response.data)
