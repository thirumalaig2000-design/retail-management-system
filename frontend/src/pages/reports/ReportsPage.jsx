import { useEffect, useMemo, useState } from 'react'
import { Alert, Box, Card, CardContent, CircularProgress, Grid, Typography } from '@mui/material'
import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { useAuth } from '../../context/AuthContext'
import { getReport } from '../../services/reportService'

const money = (value) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(Number(value || 0))

export default function ReportsPage() {
  const { user } = useAuth()
  const [data, setData] = useState(null)
  const [error, setError] = useState('')
  const admin = user?.role_code !== 'USER'

  useEffect(() => {
    const requests = [getReport('sales'), getReport('products'), getReport('payments')]
    if (admin) requests.push(getReport('inventory'), getReport('purchases'), getReport('profit'))
    Promise.all(requests)
      .then(([sales, products, payments, inventory, purchases, profit]) => setData({ sales, products, payments, inventory, purchases, profit }))
      .catch(() => setError('Unable to load reports. Please try again.'))
  }, [admin])

  const products = useMemo(() => (data?.products?.results || []).slice(0, 8).map((item) => ({ ...item, revenue: Number(item.revenue) })), [data])
  if (error) return <Alert severity="error">{error}</Alert>
  if (!data) return <Box sx={{ display: 'grid', placeItems: 'center', minHeight: 260 }}><CircularProgress /></Box>

  return (
    <Box>
      <Typography variant="h4" sx={{ color: '#fff', fontWeight: 900, mb: 1 }}>Business reports</Typography>
      <Typography sx={{ color: 'rgba(255,255,255,.7)', mb: 3 }}>Live results from completed sales, paid payments, purchases, and inventory.</Typography>
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Metric label="Sales revenue" value={money(data.sales.summary.revenue)} />
        <Metric label="Completed orders" value={data.sales.summary.orders} />
        {admin && <Metric label="Gross profit" value={money(data.profit.gross_profit)} />}
        {admin && <Metric label="Low-stock products" value={data.inventory.summary.low_stock} />}
      </Grid>
      <Grid container spacing={3}>
        <Grid item xs={12} lg={8}>
          <Panel title="Top-selling products">
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={products}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,.16)" />
                <XAxis dataKey="name" hide />
                <YAxis stroke="#b8c5db" />
                <Tooltip formatter={(value) => money(value)} />
                <Legend />
                <Bar dataKey="revenue" name="Revenue" fill="#78a6ff" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </Panel>
        </Grid>
        <Grid item xs={12} lg={4}>
          <Panel title="Payment methods">
            {data.payments.results.length ? data.payments.results.map((item) => (
              <Box key={item.payment_method} sx={{ display: 'flex', justifyContent: 'space-between', py: 1, borderBottom: '1px solid rgba(255,255,255,.08)' }}>
                <Typography>{item.payment_method}</Typography><Typography fontWeight={700}>{money(item.amount)}</Typography>
              </Box>
            )) : <Typography color="rgba(255,255,255,.65)">No paid payments in this period.</Typography>}
          </Panel>
        </Grid>
        {admin && (
          <Grid item xs={12} lg={6}><Panel title="Inventory summary"><Typography>Products tracked: <b>{data.inventory.summary.products}</b></Typography><Typography sx={{ mt: 1 }}>Stock value: <b>{money(data.inventory.summary.stock_value)}</b></Typography></Panel></Grid>
        )}
        {admin && (
          <Grid item xs={12} lg={6}><Panel title="Purchase summary"><Typography>Purchase orders: <b>{data.purchases.summary.orders}</b></Typography><Typography sx={{ mt: 1 }}>Purchased value: <b>{money(data.purchases.summary.total)}</b></Typography></Panel></Grid>
        )}
      </Grid>
    </Box>
  )
}

function Metric({ label, value }) {
  return <Grid item xs={12} sm={6} md={3}><Card sx={{ borderRadius: 3, bgcolor: 'rgba(255,255,255,.07)', color: '#fff' }}><CardContent><Typography color="rgba(255,255,255,.65)" variant="body2">{label}</Typography><Typography variant="h5" fontWeight={800} sx={{ mt: 1 }}>{value}</Typography></CardContent></Card></Grid>
}

function Panel({ title, children }) {
  return <Card sx={{ borderRadius: 3, bgcolor: 'rgba(255,255,255,.07)', color: '#fff', height: '100%' }}><CardContent><Typography variant="h6" fontWeight={800} sx={{ mb: 2 }}>{title}</Typography>{children}</CardContent></Card>
}
