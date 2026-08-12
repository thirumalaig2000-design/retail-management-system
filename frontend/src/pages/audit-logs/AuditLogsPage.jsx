import { useEffect, useMemo, useState } from 'react'
import {
  Alert,
  Box,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Grid,
  MenuItem,
  Pagination,
  Stack,
  TextField,
  Typography,
} from '@mui/material'
import PageHeader from '../../components/common/PageHeader'
import DataTable from '../../components/common/DataTable'
import { getAuditLogs } from '../../services/auditService'

const ACTIONS = ['LOGIN', 'LOGOUT', 'CREATED', 'UPDATED', 'DEACTIVATED', 'ADJUSTED', 'RECEIVED', 'COMPLETED', 'SETTINGS_UPDATED']
const MODULES = ['AUTH', 'PRODUCT', 'CATEGORY', 'CUSTOMER', 'SUPPLIER', 'INVENTORY', 'PURCHASE', 'SALE', 'USER', 'SETTINGS', 'SECURITY']

export default function AuditLogsPage() {
  const [logs, setLogs] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [page, setPage] = useState(1)
  const [search, setSearch] = useState('')
  const [module, setModule] = useState('')
  const [action, setAction] = useState('')

  useEffect(() => {
    let active = true
    setLoading(true)
    getAuditLogs({ page, search, module, action })
      .then((data) => {
        if (active) {
          setLogs(data)
          setError('')
        }
      })
      .catch(() => {
        if (active) setError('Unable to load audit logs right now.')
      })
      .finally(() => {
        if (active) setLoading(false)
      })
    return () => {
      active = false
    }
  }, [page, search, module, action])

  const rows = useMemo(
    () =>
      (logs?.results || []).map((item) => ({
        ...item,
        id: item.id,
      })),
    [logs],
  )

  if (error) {
    return <Alert severity="error">{error}</Alert>
  }

  return (
    <Box>
      <PageHeader
        title="Audit logs"
        description="Track sensitive actions across authentication, inventory, sales, purchases, and settings."
      />

      <Card sx={panelSx}>
        <CardContent>
          <Stack spacing={2} sx={{ mb: 3 }}>
            <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.72)' }}>
              Search by user, record id, or description. Logs are ordered by newest first.
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} md={5}>
                <TextField
                  label="Search"
                  value={search}
                  onChange={(event) => {
                    setPage(1)
                    setSearch(event.target.value)
                  }}
                  fullWidth
                />
              </Grid>
              <Grid item xs={12} md={3}>
                <TextField
                  select
                  label="Module"
                  value={module}
                  onChange={(event) => {
                    setPage(1)
                    setModule(event.target.value)
                  }}
                  fullWidth
                >
                  <MenuItem value="">All modules</MenuItem>
                  {MODULES.map((item) => (
                    <MenuItem key={item} value={item}>
                      {item}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={12} md={3}>
                <TextField
                  select
                  label="Action"
                  value={action}
                  onChange={(event) => {
                    setPage(1)
                    setAction(event.target.value)
                  }}
                  fullWidth
                >
                  <MenuItem value="">All actions</MenuItem>
                  {ACTIONS.map((item) => (
                    <MenuItem key={item} value={item}>
                      {item}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
            </Grid>
          </Stack>

          {loading && !logs ? (
            <Box sx={{ display: 'grid', placeItems: 'center', minHeight: 220 }}>
              <CircularProgress />
            </Box>
          ) : (
            <>
              <DataTable
                rows={rows}
                columns={[
                  { key: 'created_at', label: 'Time', render: (row) => new Date(row.created_at).toLocaleString() },
                  { key: 'user_name', label: 'User', render: (row) => row.user_name || row.user_email || 'System' },
                  { key: 'module', label: 'Module', render: (row) => <Chip size="small" label={row.module} variant="outlined" /> },
                  { key: 'action', label: 'Action', render: (row) => <Chip size="small" label={row.action} color="primary" /> },
                  { key: 'record_id', label: 'Record', render: (row) => row.record_id || '—' },
                  { key: 'description', label: 'Description' },
                ]}
                emptyText="No matching audit logs."
              />

              <Stack direction={{ xs: 'column', sm: 'row' }} justifyContent="space-between" alignItems={{ xs: 'flex-start', sm: 'center' }} spacing={2} sx={{ mt: 3 }}>
                <Typography sx={{ color: 'rgba(255,255,255,0.72)' }}>
                  Showing {rows.length} of {logs?.count || 0} entries
                </Typography>
                <Pagination
                  count={Math.max(1, Math.ceil((logs?.count || 0) / 20))}
                  page={page}
                  onChange={(_, value) => setPage(value)}
                  color="primary"
                />
              </Stack>
            </>
          )}
        </CardContent>
      </Card>
    </Box>
  )
}

const panelSx = {
  borderRadius: 4,
  bgcolor: 'rgba(255,255,255,0.06)',
  color: '#fff',
  border: '1px solid rgba(255,255,255,0.08)',
  backdropFilter: 'blur(14px)',
}
