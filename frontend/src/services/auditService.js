import api from './api'

export const getAuditLogs = (params = {}) => api.get('/audit-logs/', { params }).then((response) => response.data)
export const getSecurityReview = () => api.get('/security/review/').then((response) => response.data)
