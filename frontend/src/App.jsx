import { Navigate, Route, Routes } from 'react-router-dom'
import { Box } from '@mui/material'
import { useAuth } from './context/AuthContext'
import { ROLE_HOME, ROLES } from './constants/roles'
import AppShell from './components/layout/AppShell'
import LoginPage from './pages/auth/LoginPage'
import DashboardPage from './pages/dashboard/DashboardPage'
import ProductsPage from './pages/products/ProductsPage'
import CategoriesPage from './pages/categories/CategoriesPage'
import CustomersPage from './pages/customers/CustomersPage'
import SuppliersPage from './pages/suppliers/SuppliersPage'
import InventoryPage from './pages/inventory/InventoryPage'
import PurchasesPage from './pages/purchases/PurchasesPage'
import PosPage from './pages/pos/PosPage'
import SalesPage from './pages/sales/SalesPage'
import InvoicesPage from './pages/invoices/InvoicesPage'
import ReportsPage from './pages/reports/ReportsPage'
import AuditLogsPage from './pages/audit-logs/AuditLogsPage'
import SettingsPage from './pages/settings/SettingsPage'
import ProtectedRoute from './routes/ProtectedRoute'
import RoleProtectedRoute from './routes/RoleProtectedRoute'
import UnauthorizedPage from './pages/unauthorized/UnauthorizedPage'

function App() {
  const { user } = useAuth()

  return (
    <Box sx={{ minHeight: '100vh' }}>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/unauthorized" element={<UnauthorizedPage />} />
        <Route element={<ProtectedRoute />}>
          <Route element={<AppShell />}>
            <Route
              path="/"
              element={<Navigate to={ROLE_HOME[user?.role_code] || '/login'} replace />}
            />
            <Route
              element={<RoleProtectedRoute allowedRoles={[ROLES.SUPER_ADMIN]} />}
            >
              <Route path="/super-admin/dashboard" element={<DashboardPage />} />
              <Route path="/super-admin/inventory" element={<InventoryPage />} />
              <Route path="/super-admin/purchases" element={<PurchasesPage />} />
              <Route path="/super-admin/pos" element={<PosPage />} />
              <Route path="/super-admin/sales" element={<SalesPage />} />
              <Route path="/super-admin/invoices" element={<InvoicesPage />} />
              <Route path="/super-admin/products" element={<ProductsPage />} />
              <Route path="/super-admin/categories" element={<CategoriesPage />} />
              <Route path="/super-admin/customers" element={<CustomersPage />} />
              <Route path="/super-admin/suppliers" element={<SuppliersPage />} />
              <Route path="/super-admin/reports" element={<ReportsPage />} />
              <Route path="/super-admin/audit-logs" element={<AuditLogsPage />} />
              <Route path="/super-admin/settings" element={<SettingsPage />} />
            </Route>
            <Route element={<RoleProtectedRoute allowedRoles={[ROLES.ADMIN]} />}>
              <Route path="/admin/dashboard" element={<DashboardPage />} />
              <Route path="/admin/inventory" element={<InventoryPage />} />
              <Route path="/admin/purchases" element={<PurchasesPage />} />
              <Route path="/admin/pos" element={<PosPage />} />
              <Route path="/admin/sales" element={<SalesPage />} />
              <Route path="/admin/invoices" element={<InvoicesPage />} />
              <Route path="/admin/products" element={<ProductsPage />} />
              <Route path="/admin/categories" element={<CategoriesPage />} />
              <Route path="/admin/customers" element={<CustomersPage />} />
              <Route path="/admin/suppliers" element={<SuppliersPage />} />
              <Route path="/admin/reports" element={<ReportsPage />} />
              <Route path="/admin/audit-logs" element={<AuditLogsPage />} />
            </Route>
            <Route element={<RoleProtectedRoute allowedRoles={[ROLES.USER]} />}>
              <Route path="/user/dashboard" element={<DashboardPage />} />
              <Route path="/user/inventory" element={<InventoryPage />} />
              <Route path="/user/pos" element={<PosPage />} />
              <Route path="/user/sales" element={<SalesPage />} />
              <Route path="/user/invoices" element={<InvoicesPage />} />
              <Route path="/user/products" element={<ProductsPage />} />
              <Route path="/user/customers" element={<CustomersPage />} />
              <Route path="/user/reports" element={<ReportsPage />} />
            </Route>
          </Route>
        </Route>
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </Box>
  )
}

export default App
