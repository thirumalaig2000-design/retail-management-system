import { useEffect, useState } from 'react'
import { Alert, Box, Card, CardContent, CircularProgress, Grid, Typography } from '@mui/material'
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { useAuth } from '../../context/AuthContext'
import { getDashboard } from '../../services/reportService'

const money = (value) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(Number(value || 0))
export default function DashboardPage() {
  const { user } = useAuth(); const [dashboard, setDashboard] = useState(null); const [error, setError] = useState('')
  useEffect(() => { getDashboard().then(setDashboard).catch(() => setError('Unable to load dashboard data.')) }, [])
  if (error) return <Alert severity="error">{error}</Alert>
  if (!dashboard) return <Box sx={{ display: 'grid', placeItems: 'center', minHeight: 260 }}><CircularProgress /></Box>
  const metrics = [['Today sales', money(dashboard.today_sales)], ['Monthly sales', money(dashboard.monthly_sales)], ['Completed orders', dashboard.total_orders], [user?.role_code === 'USER' ? 'Gross profit' : 'Low stock', user?.role_code === 'USER' ? money(dashboard.gross_profit) : dashboard.low_stock]]
  return <Box><Typography variant="h4" sx={{ color: '#fff', fontWeight: 900, mb: 1 }}>Welcome back, {user?.full_name || user?.email}</Typography><Typography sx={{ color: 'rgba(255,255,255,.7)', mb: 3 }}>You are signed in as {user?.role_code?.replaceAll('_', ' ')}.</Typography><Grid container spacing={2}>{metrics.map(([label, value]) => <Grid item xs={12} sm={6} md={3} key={label}><Card sx={{ borderRadius: 4, bgcolor: 'rgba(255,255,255,.06)', color: '#fff', border: '1px solid rgba(255,255,255,.08)' }}><CardContent><Typography variant="body2" color="rgba(255,255,255,.65)">{label}</Typography><Typography variant="h4" sx={{ mt: 1, fontWeight: 800 }}>{value}</Typography></CardContent></Card></Grid>)}</Grid><Card sx={{ mt: 3, borderRadius: 4, bgcolor: 'rgba(255,255,255,.06)', color: '#fff' }}><CardContent><Typography fontWeight={800} sx={{ mb: 2 }}>Sales this month</Typography><ResponsiveContainer width="100%" height={280}><AreaChart data={dashboard.sales_chart.map((x) => ({ ...x, revenue: Number(x.revenue) }))}><CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,.14)" /><XAxis dataKey="date" stroke="#b8c5db" /><YAxis stroke="#b8c5db" /><Tooltip formatter={(value) => money(value)} /><Area type="monotone" dataKey="revenue" stroke="#78a6ff" fill="#78a6ff55" /></AreaChart></ResponsiveContainer></CardContent></Card></Box>
}
