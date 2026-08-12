import { useEffect, useState } from 'react'
import { Alert, Box } from '@mui/material'
import PageHeader from '../../components/common/PageHeader'
import SearchInput from '../../components/common/SearchInput'
import DataTable from '../../components/common/DataTable'
import { invoiceService } from '../../services/invoiceService'

export default function InvoicesPage() {
  const [items, setItems] = useState([])
  const [search, setSearch] = useState('')
  const [error, setError] = useState('')

  async function loadData() {
    try {
      const response = await invoiceService.list({ search })
      setItems(response.results || [])
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load invoices.')
    }
  }

  useEffect(() => {
    loadData()
  }, [search])

  return (
    <Box>
      <PageHeader title="Invoices" description="Search and review invoice history." />
      {error ? <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert> : null}
      <SearchInput value={search} onChange={setSearch} placeholder="Search invoices..." />
      <DataTable
        rows={items}
        columns={[
          { key: 'invoice_number', label: 'Invoice #' },
          { key: 'sale_number', label: 'Sale #' },
          { key: 'customer_name', label: 'Customer' },
          { key: 'payment_method', label: 'Payment Method' },
          { key: 'issued_at', label: 'Issued At' },
        ]}
        emptyText="No invoices found."
      />
    </Box>
  )
}
