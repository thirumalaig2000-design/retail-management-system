import { TextField } from '@mui/material'

export default function SearchInput({ value, onChange, placeholder = 'Search...' }) {
  return (
    <TextField
      value={value}
      onChange={(event) => onChange(event.target.value)}
      placeholder={placeholder}
      fullWidth
      size="small"
      sx={{
        mb: 2,
        maxWidth: 420,
        '& .MuiInputBase-root': { bgcolor: 'rgba(255,255,255,0.04)' },
      }}
    />
  )
}
