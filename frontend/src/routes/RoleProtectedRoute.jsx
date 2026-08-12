import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { ROLE_HOME, ROLES } from '../constants/roles'

export default function RoleProtectedRoute({ allowedRoles }) {
  const { user } = useAuth()

  if (!user) {
    return <Navigate to="/login" replace />
  }

  if (user.role_code !== ROLES.SUPER_ADMIN && !allowedRoles.includes(user.role_code)) {
    return <Navigate to={ROLE_HOME[user.role_code] || '/login'} replace />
  }

  return <Outlet />
}
