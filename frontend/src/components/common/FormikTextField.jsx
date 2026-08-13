import { TextField } from '@mui/material'
import { useField } from 'formik'

export default function FormikTextField({ name, helperText, ...props }) {
  const [field, meta] = useField(name)
  const showError = meta.touched && Boolean(meta.error)

  return (
    <TextField
      {...field}
      {...props}
      error={showError}
      helperText={showError ? meta.error : helperText}
    />
  )
}
