export const ROLES = {
  SUPER_ADMIN: 'SUPER_ADMIN',
  ADMIN: 'ADMIN',
  USER: 'USER',
}

export const ROLE_HOME = {
  [ROLES.SUPER_ADMIN]: '/super-admin/dashboard',
  [ROLES.ADMIN]: '/admin/dashboard',
  [ROLES.USER]: '/user/dashboard',
}
