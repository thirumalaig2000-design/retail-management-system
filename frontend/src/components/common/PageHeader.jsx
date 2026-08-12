import { Box, Button, Typography } from '@mui/material'

export default function PageHeader({ title, description, actionLabel, onAction, actionDisabled }) {
  return (
    <Box
      sx={{
        display: 'flex',
        gap: 2,
        alignItems: { xs: 'flex-start', md: 'center' },
        justifyContent: 'space-between',
        flexDirection: { xs: 'column', md: 'row' },
        mb: 3,
      }}
    >
      <Box>
        <Typography variant="h4" sx={{ color: '#fff', fontWeight: 900 }}>
          {title}
        </Typography>
        {description ? (
          <Typography sx={{ color: 'rgba(255,255,255,0.7)', mt: 0.5 }}>{description}</Typography>
        ) : null}
      </Box>
      {actionLabel ? (
        <Button variant="contained" onClick={onAction} disabled={actionDisabled}>
          {actionLabel}
        </Button>
      ) : null}
    </Box>
  )
}
