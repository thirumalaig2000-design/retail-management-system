import {
  Box,
  Button,
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from '@mui/material'
import StatusChip from './StatusChip'

export default function DataTable({
  rows,
  columns,
  onEdit,
  onDelete,
  onToggle,
  onToggleLabel,
  onToggleDisabled,
  emptyText,
}) {
  return (
    <TableContainer
      component={Paper}
      sx={{
        bgcolor: 'rgba(255,255,255,0.04)',
        border: '1px solid rgba(255,255,255,0.08)',
        borderRadius: 3,
      }}
    >
      <Table>
        <TableHead>
          <TableRow>
            {columns.map((column) => (
              <TableCell key={column.key} sx={{ color: 'rgba(255,255,255,0.78)', fontWeight: 700 }}>
                {column.label}
              </TableCell>
            ))}
            {(onEdit || onDelete || onToggle) ? (
              <TableCell sx={{ color: 'rgba(255,255,255,0.78)', fontWeight: 700 }}>
                Actions
              </TableCell>
            ) : null}
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.length === 0 ? (
            <TableRow>
              <TableCell colSpan={columns.length + 1}>
                <Box sx={{ py: 4, textAlign: 'center' }}>
                  <Typography sx={{ color: 'rgba(255,255,255,0.7)' }}>
                    {emptyText || 'No records found.'}
                  </Typography>
                </Box>
              </TableCell>
            </TableRow>
          ) : (
            rows.map((row) => (
              <TableRow key={row.id} hover>
                {columns.map((column) => (
                  <TableCell key={column.key} sx={{ color: '#fff' }}>
                    {column.render ? column.render(row) : row[column.key]}
                  </TableCell>
                ))}
                {(onEdit || onDelete || onToggle) ? (
                  <TableCell>
                    <Stack direction="row" spacing={1} useFlexGap flexWrap="wrap">
                      {onToggle ? (
                        <Button
                          size="small"
                          variant="outlined"
                          onClick={() => onToggle(row)}
                          disabled={onToggleDisabled ? onToggleDisabled(row) : false}
                        >
                          {typeof onToggleLabel === 'function'
                            ? onToggleLabel(row)
                            : onToggleLabel || (row.is_active ? 'Deactivate' : 'Activate')}
                        </Button>
                      ) : null}
                      {onEdit ? (
                        <Button size="small" variant="outlined" onClick={() => onEdit(row)}>
                          Edit
                        </Button>
                      ) : null}
                      {onDelete ? (
                        <Button size="small" color="error" variant="outlined" onClick={() => onDelete(row)}>
                          Delete
                        </Button>
                      ) : null}
                    </Stack>
                  </TableCell>
                ) : null}
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
    </TableContainer>
  )
}
