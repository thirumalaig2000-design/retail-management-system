import { AppBar, Box, Button, Drawer, List, ListItemButton, ListItemText, Toolbar, Typography } from '@mui/material'
import { NavLink, Outlet } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'

const drawerWidth = 260

const navByRole = {
  SUPER_ADMIN: [
    ['Dashboard', '/super-admin/dashboard'],
    ['Inventory', '/super-admin/inventory'],
    ['Purchases', '/super-admin/purchases'],
    ['POS', '/super-admin/pos'],
    ['Sales', '/super-admin/sales'],
    ['Invoices', '/super-admin/invoices'],
    ['Products', '/super-admin/products'],
    ['Categories', '/super-admin/categories'],
    ['Customers', '/super-admin/customers'],
    ['Suppliers', '/super-admin/suppliers'],
    ['Reports', '/super-admin/reports'],
    ['Audit Logs', '/super-admin/audit-logs'],
    ['Settings', '/super-admin/settings'],
  ],
  ADMIN: [
    ['Dashboard', '/admin/dashboard'],
    ['Inventory', '/admin/inventory'],
    ['Purchases', '/admin/purchases'],
    ['POS', '/admin/pos'],
    ['Sales', '/admin/sales'],
    ['Invoices', '/admin/invoices'],
    ['Products', '/admin/products'],
    ['Categories', '/admin/categories'],
    ['Customers', '/admin/customers'],
    ['Suppliers', '/admin/suppliers'],
    ['Reports', '/admin/reports'],
    ['Audit Logs', '/admin/audit-logs'],
  ],
  USER: [
    ['Dashboard', '/user/dashboard'],
    ['Inventory', '/user/inventory'],
    ['POS', '/user/pos'],
    ['Sales', '/user/sales'],
    ['Invoices', '/user/invoices'],
    ['Products', '/user/products'],
    ['Customers', '/user/customers'],
    ['Reports', '/user/reports'],
  ],
}

export default function AppShell() {
  const { user, logout } = useAuth()
  const links = navByRole[user?.role_code] || []

  return (
    <Box
      sx={{
        display: 'flex',
        minHeight: '100vh',
        bgcolor: '#07111f',
        backgroundImage:
          'radial-gradient(circle at top left, rgba(120,166,255,0.16), transparent 28%), radial-gradient(circle at top right, rgba(90,228,196,0.10), transparent 24%), linear-gradient(180deg, #09111f 0%, #07111f 100%)',
      }}
    >
      <AppBar
        position="fixed"
        elevation={0}
        sx={{
          ml: `${drawerWidth}px`,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          bgcolor: 'rgba(7, 17, 31, 0.88)',
          backdropFilter: 'blur(18px)',
          borderBottom: '1px solid rgba(255,255,255,0.08)',
          backgroundImage: 'linear-gradient(180deg, rgba(7,17,31,0.96), rgba(7,17,31,0.82))',
        }}
      >
        <Toolbar sx={{ justifyContent: 'space-between' }}>
          <Box>
            <Typography variant="h6" sx={{ fontWeight: 800, letterSpacing: 0.4 }}>
              SmartStock
            </Typography>
            <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.7)' }}>
              {user?.role_code?.replaceAll('_', ' ')}
            </Typography>
          </Box>
          <Button color="inherit" variant="outlined" onClick={logout}>
            Logout
          </Button>
        </Toolbar>
      </AppBar>

      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
            bgcolor: '#0b1528',
            color: 'white',
            borderRight: '1px solid rgba(255,255,255,0.08)',
            backgroundImage:
              'linear-gradient(180deg, rgba(11,21,40,0.96), rgba(9,17,31,0.98))',
          },
        }}
      >
        <Toolbar sx={{ px: 3, py: 2 }}>
          <Box>
            <Typography variant="h5" sx={{ fontWeight: 900 }}>
              SmartStock
            </Typography>
            <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)' }}>
              Retail management core
            </Typography>
          </Box>
        </Toolbar>
        <List sx={{ px: 1 }}>
          {links.map(([label, to]) => (
            <ListItemButton
              key={label}
              component={NavLink}
              to={to}
              sx={{
                borderRadius: 2,
                mx: 1,
                my: 0.5,
                '&.active': {
                  bgcolor: 'rgba(120, 166, 255, 0.14)',
                },
              }}
            >
              <ListItemText primary={label} />
            </ListItemButton>
          ))}
        </List>
        <Box sx={{ mt: 'auto', px: 3, pb: 3 }}>
          <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)' }}>
            Signed in as
          </Typography>
          <Typography variant="subtitle2" sx={{ fontWeight: 700 }}>
            {user?.full_name || user?.email}
          </Typography>
          <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.55)' }}>
            {user?.role_code?.replaceAll('_', ' ')}
          </Typography>
        </Box>
      </Drawer>

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: { xs: 2, md: 4 },
          ml: `${drawerWidth}px`,
          width: `calc(100% - ${drawerWidth}px)`,
        }}
      >
        <Toolbar />
        <Outlet />
      </Box>
    </Box>
  )
}
