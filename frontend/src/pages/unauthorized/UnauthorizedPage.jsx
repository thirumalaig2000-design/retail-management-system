import { Box, Button, Typography } from '@mui/material'
import { Link } from 'react-router-dom'

export default function UnauthorizedPage() {
  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'grid',
        placeItems: 'center',
        bgcolor: '#08111f',
        color: '#fff',
        textAlign: 'center',
        px: 2,
      }}
    >
      <Box>
        <Typography variant="h3" sx={{ fontWeight: 900, mb: 2 }}>
          Access denied
        </Typography>
        <Typography sx={{ color: 'rgba(255,255,255,0.72)', mb: 3 }}>
          Your account does not have permission to open this page.
        </Typography>
        <Button component={Link} to="/" variant="contained">
          Go home
        </Button>
      </Box>
    </Box>
  )
}
