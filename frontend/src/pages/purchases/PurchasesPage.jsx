import { useEffect, useMemo, useState } from 'react'
import { Alert, Box, Button, MenuItem, Stack, TextField, Typography } from '@mui/material'
import PageHeader from '../../components/common/PageHeader'
import SearchInput from '../../components/common/SearchInput'
import DataTable from '../../components/common/DataTable'
import EntityDialog from '../../components/common/EntityDialog'
import StatusChip from '../../components/common/StatusChip'
import { useAuth } from '../../context/AuthContext'
import { ROLES } from '../../constants/roles'
import { purchaseService } from '../../services/purchaseService'
import { supplierService } from '../../services/supplierService'
import { productService } from '../../services/productService'

const blankItem = { product: '', quantity: '', unit_price: '', tax_percentage: '' }

export default function PurchasesPage() {
  const { user } = useAuth()
  const canManage = user?.role_code !== ROLES.USER
  const [items, setItems] = useState([])
  const [suppliers, setSuppliers] = useState([])
  const [products, setProducts] = useState([])
  const [search, setSearch] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [dialogOpen, setDialogOpen] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [form, setForm] = useState({
    supplier: '',
    purchase_date: new Date().toISOString().slice(0, 10),
    status: 'ORDERED',
    items: [{ ...blankItem }],
  })

  async function loadData() {
    setLoading(true)
    setError('')
    try {
      const [purchaseResponse, supplierResponse, productResponse] = await Promise.all([
        purchaseService.list({ search }),
        canManage ? supplierService.list({ status: 'active' }) : Promise.resolve({ results: [] }),
        canManage ? productService.list({ status: 'active' }) : Promise.resolve({ results: [] }),
      ])
      setItems(purchaseResponse.results || [])
      setSuppliers(supplierResponse.results || [])
      setProducts(productResponse.results || [])
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load purchases.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData()
  }, [search, canManage])

  const totalItems = useMemo(() => form.items.length, [form.items])

  function openCreate() {
    setForm({
      supplier: '',
      purchase_date: new Date().toISOString().slice(0, 10),
      status: 'ORDERED',
      items: [{ ...blankItem }],
    })
    setDialogOpen(true)
  }

  function updateItem(index, patch) {
    setForm((current) => ({
      ...current,
      items: current.items.map((item, itemIndex) => (itemIndex === index ? { ...item, ...patch } : item)),
    }))
  }

  function addItem() {
    setForm((current) => ({ ...current, items: [...current.items, { ...blankItem }] }))
  }

  function removeItem(index) {
    setForm((current) => ({
      ...current,
      items: current.items.length === 1 ? current.items : current.items.filter((_, itemIndex) => itemIndex !== index),
    }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setSubmitting(true)
    try {
      const payload = {
        supplier: Number(form.supplier),
        purchase_date: form.purchase_date,
        status: form.status,
        items: form.items.map((item) => ({
          product: Number(item.product),
          quantity: item.quantity,
          unit_price: item.unit_price || undefined,
          tax_percentage: item.tax_percentage || undefined,
        })),
      }
      await purchaseService.create(payload)
      setDialogOpen(false)
      await loadData()
    } catch (err) {
      setError(err.response?.data?.detail || 'Unable to save purchase.')
    } finally {
      setSubmitting(false)
    }
  }

  async function handleReceive(row) {
    if (!window.confirm(`Receive ${row.purchase_number}?`)) return
    await purchaseService.receive(row.id, {})
    loadData()
  }

  return (
    <Box>
      <PageHeader
        title="Purchases"
        description="Create purchase orders and receive stock into inventory."
        actionLabel={canManage ? 'New Purchase' : ''}
        onAction={canManage ? openCreate : undefined}
      />
      {error ? <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert> : null}
      <SearchInput value={search} onChange={setSearch} placeholder="Search purchases..." />
      <DataTable
        rows={items}
        columns={[
          { key: 'purchase_number', label: 'Purchase #' },
          { key: 'supplier_name', label: 'Supplier' },
          { key: 'purchase_date', label: 'Date' },
          { key: 'status', label: 'Status', render: (row) => <StatusChip active={row.status === 'RECEIVED'} /> },
          { key: 'total', label: 'Total' },
        ]}
        onToggle={canManage ? (row) => handleReceive(row) : undefined}
        onToggleLabel={() => 'Receive'}
        onToggleDisabled={(row) => row.status === 'RECEIVED'}
        emptyText={loading ? 'Loading purchases...' : 'No purchases found.'}
      />

      {canManage ? (
        <EntityDialog
          open={dialogOpen}
          title="Create Purchase"
          onClose={() => setDialogOpen(false)}
          onSubmit={handleSubmit}
          submitting={submitting}
        >
          <TextField
            select
            label="Supplier"
            value={form.supplier}
            onChange={(e) => setForm({ ...form, supplier: e.target.value })}
            required
          >
            <MenuItem value="">Select supplier</MenuItem>
            {suppliers.map((supplier) => (
              <MenuItem key={supplier.id} value={supplier.id}>{supplier.name}</MenuItem>
            ))}
          </TextField>
          <TextField
            label="Purchase Date"
            type="date"
            value={form.purchase_date}
            onChange={(e) => setForm({ ...form, purchase_date: e.target.value })}
            InputLabelProps={{ shrink: true }}
          />
          <TextField
            select
            label="Status"
            value={form.status}
            onChange={(e) => setForm({ ...form, status: e.target.value })}
          >
            <MenuItem value="DRAFT">Draft</MenuItem>
            <MenuItem value="ORDERED">Ordered</MenuItem>
          </TextField>

          <Box sx={{ display: 'grid', gap: 2 }}>
            <Typography variant="subtitle2">Items ({totalItems})</Typography>
            {form.items.map((item, index) => (
              <Box key={index} sx={{ p: 2, border: '1px solid rgba(255,255,255,0.08)', borderRadius: 2 }}>
                <Stack spacing={2}>
                  <TextField
                    select
                    label="Product"
                    value={item.product}
                    onChange={(e) => updateItem(index, { product: e.target.value })}
                    required
                  >
                    <MenuItem value="">Select product</MenuItem>
                    {products.map((product) => (
                      <MenuItem key={product.id} value={product.id}>{product.name} ({product.sku})</MenuItem>
                    ))}
                  </TextField>
                  <TextField
                    label="Quantity"
                    type="number"
                    value={item.quantity}
                    onChange={(e) => updateItem(index, { quantity: e.target.value })}
                    required
                  />
                  <TextField
                    label="Unit Price"
                    type="number"
                    value={item.unit_price}
                    onChange={(e) => updateItem(index, { unit_price: e.target.value })}
                  />
                  <TextField
                    label="Tax %"
                    type="number"
                    value={item.tax_percentage}
                    onChange={(e) => updateItem(index, { tax_percentage: e.target.value })}
                  />
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Button
                      variant="outlined"
                      onClick={addItem}
                      type="button"
                    >
                      Add item
                    </Button>
                    {form.items.length > 1 ? (
                      <Button color="error" variant="outlined" onClick={() => removeItem(index)} type="button">
                        Remove
                      </Button>
                    ) : null}
                  </Box>
                </Stack>
              </Box>
            ))}
          </Box>
        </EntityDialog>
      ) : null}
    </Box>
  )
}
