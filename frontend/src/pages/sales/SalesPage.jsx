import { useEffect, useState } from 'react'
import { Alert, Box } from '@mui/material'
import PageHeader from '../../components/common/PageHeader'
import SearchInput from '../../components/common/SearchInput'
import DataTable from '../../components/common/DataTable'
import { salesService } from '../../services/salesService'

export default function SalesPage() {
  const [items, setItems] = useState([])
  const [search, setSearch] = useState('')
  const [error, setError] = useState('')

  async function loadData() {
    try {
      const response = await salesService.list({ search })
      setItems(response.results || [])
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load sales.')
    }
  }

  useEffect(() => {
    loadData()
  }, [search])

  return (
    <Box>
      <PageHeader title="Sales" description="Browse completed and pending sales." />
      {error ? <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert> : null}
      <SearchInput value={search} onChange={setSearch} placeholder="Search sales..." />
      <DataTable
        rows={items}
        columns={[
          { key: 'sale_number', label: 'Sale #' },
          { key: 'customer_name', label: 'Customer' },
          { key: 'cashier_email', label: 'Cashier' },
          { key: 'status', label: 'Status' },
          { key: 'grand_total', label: 'Grand Total' },
        ]}
        emptyText="No sales found."
      />
    </Box>
  )
}
