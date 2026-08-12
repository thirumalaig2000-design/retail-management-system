import { Button, Dialog, DialogActions, DialogContent, DialogTitle, Stack } from '@mui/material'

export default function EntityDialog({ open, title, onClose, onSubmit, submitting, children }) {
  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>{title}</DialogTitle>
      <DialogContent>
        <Stack component="form" onSubmit={onSubmit} spacing={2} sx={{ pt: 1 }}>
          {children}
          <DialogActions sx={{ px: 0 }}>
            <Button onClick={onClose} disabled={submitting}>
              Cancel
            </Button>
            <Button type="submit" variant="contained" disabled={submitting}>
              {submitting ? 'Saving...' : 'Save'}
            </Button>
          </DialogActions>
        </Stack>
      </DialogContent>
    </Dialog>
  )
}
