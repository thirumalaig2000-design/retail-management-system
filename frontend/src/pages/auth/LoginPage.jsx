import { useState } from 'react'
import { Form, Formik } from 'formik'
import * as Yup from 'yup'
import { Alert, Box, Button, Card, CardContent, Container, TextField, Typography } from '@mui/material'
import { useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import { ROLE_HOME } from '../../constants/roles'
import FormikTextField from '../../components/common/FormikTextField'

const loginSchema = Yup.object({
  email: Yup.string().trim().email('Enter a valid email address.').required('Email is required.'),
  password: Yup.string().required('Password is required.'),
})

export default function LoginPage() {
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login, user } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  const from = location.state?.from?.pathname || ROLE_HOME[user?.role_code] || '/login'

  async function handleSubmit(values) {
    setLoading(true)
    setError('')
    try {
      const session = await login(values.email, values.password)
      navigate(ROLE_HOME[session.user.role_code] || '/', { replace: true })
    } catch (err) {
      setError(err.response?.data?.detail || 'Unable to sign in. Check your credentials.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'grid',
        placeItems: 'center',
        px: 2,
        background:
          'radial-gradient(circle at top left, rgba(77, 144, 255, 0.32), transparent 30%), linear-gradient(160deg, #050b16 0%, #0a1830 45%, #101d34 100%)',
      }}
    >
      <Container maxWidth="sm">
        <Card
          sx={{
            borderRadius: 5,
            bgcolor: 'rgba(11, 21, 40, 0.88)',
            color: '#fff',
            border: '1px solid rgba(255,255,255,0.08)',
            boxShadow: '0 24px 70px rgba(0,0,0,0.4)',
            backdropFilter: 'blur(18px)',
          }}
        >
          <CardContent sx={{ p: { xs: 3, md: 5 } }}>
            <Typography variant="overline" sx={{ color: '#7fb2ff', letterSpacing: 2 }}>
              SMARTSTOCK RETAIL
            </Typography>
            <Typography variant="h3" sx={{ fontWeight: 900, mt: 1, mb: 1 }}>
              Sign in to continue
            </Typography>
            <Typography sx={{ color: 'rgba(255,255,255,0.7)', mb: 3 }}>
              Use the development demo accounts seeded in PostgreSQL to enter the system.
            </Typography>

            {error ? (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            ) : null}

            <Formik initialValues={{ email: 'superadmin@smartstock.local', password: 'SmartStock!123' }} validationSchema={loginSchema} onSubmit={handleSubmit}>
              <Box component={Form} sx={{ display: 'grid', gap: 2 }}>
                <FormikTextField name="email" label="Email" fullWidth autoComplete="email" sx={{ input: { color: '#fff' }, label: { color: 'rgba(255,255,255,0.7)' } }} />
                <FormikTextField name="password" label="Password" type="password" fullWidth autoComplete="current-password" sx={{ input: { color: '#fff' }, label: { color: 'rgba(255,255,255,0.7)' } }} />
                <Button type="submit" variant="contained" size="large" disabled={loading}>
                  {loading ? 'Signing in...' : 'Login'}
                </Button>
              </Box>
            </Formik>

            <Box sx={{ mt: 3, color: 'rgba(255,255,255,0.75)' }}>
              <Typography variant="body2">Demo credentials:</Typography>
              <Typography variant="body2">superadmin@smartstock.local / SmartStock!123</Typography>
              <Typography variant="body2">admin@smartstock.local / SmartStock!123</Typography>
              <Typography variant="body2">cashier@smartstock.local / SmartStock!123</Typography>
            </Box>

            <Typography variant="caption" sx={{ display: 'block', mt: 3, color: 'rgba(255,255,255,0.5)' }}>
              Redirect target after login: {from}
            </Typography>
          </CardContent>
        </Card>
      </Container>
    </Box>
  )
}
