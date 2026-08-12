import { useEffect, useMemo, useState } from 'react'
import { Alert, Box, MenuItem, TextField } from '@mui/material'
import PageHeader from '../../components/common/PageHeader'
import SearchInput from '../../components/common/SearchInput'
import DataTable from '../../components/common/DataTable'
import EntityDialog from '../../components/common/EntityDialog'
import StatusChip from '../../components/common/StatusChip'
import { useAuth } from '../../context/AuthContext'
import { ROLES } from '../../constants/roles'
import { inventoryService } from '../../services/inventoryService'
import { categoryService } from '../../services/categoryService'
import { productService } from '../../services/productService'

const emptyAdjustment = {
  product_id: '',
  quantity: '',
  direction: 'ADJUSTMENT_OUT',
  reason: '',
}

export default function InventoryPage() {
  const { user } = useAuth()
  const canAdjust = user?.role_code !== ROLES.USER
  const [inventory, setInventory] = useState([])
  const [transactions, setTransactions] = useState([])
  const [products, setProducts] = useState([])
  const [categories, setCategories] = useState([])
  const [search, setSearch] = useState('')
  const [categoryFilter, setCategoryFilter] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [dialogOpen, setDialogOpen] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [adjustment, setAdjustment] = useState(emptyAdjustment)

  async function loadData() {
    setLoading(true)
    setError('')
    try {
      const inventoryPromise = inventoryService.list({
        search,
        category: categoryFilter || undefined,
      })
      const categoryPromise = canAdjust
        ? categoryService.list({ status: 'active' })
        : Promise.resolve({ results: [] })
      const productPromise = canAdjust
        ? productService.list({ status: 'active' })
        : Promise.resolve({ results: [] })
      const transactionPromise = canAdjust
        ? inventoryService.transactions({ search })
        : Promise.resolve({ results: [] })

      const [inventoryResponse, categoryResponse, productResponse, transactionResponse] = await Promise.all([
        inventoryPromise,
        categoryPromise,
        productPromise,
        transactionPromise,
      ])
      setInventory(inventoryResponse.results || [])
      setCategories(categoryResponse.results || [])
      setProducts(productResponse.results || [])
      setTransactions(transactionResponse.results || [])
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load inventory.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData()
  }, [search, categoryFilter, canAdjust])

  function openAdjustment(row) {
    setAdjustment({
      ...emptyAdjustment,
      product_id: row.product?.id || '',
    })
    setDialogOpen(true)
  }

  async function handleAdjustmentSubmit(event) {
    event.preventDefault()
    setSubmitting(true)
    try {
      await inventoryService.adjust({
        ...adjustment,
        quantity: Number(adjustment.quantity).toFixed(2),
      })
      setDialogOpen(false)
      await loadData()
    } catch (err) {
      setError(err.response?.data?.detail || 'Unable to adjust stock.')
    } finally {
      setSubmitting(false)
    }
  }

  const lowStockCount = useMemo(
    () => inventory.filter((item) => item.low_stock).length,
    [inventory],
  )

  return (
    <Box>
      <PageHeader
        title="Inventory"
        description="Track live stock, low-stock items, and stock adjustment history."
        actionLabel={canAdjust ? 'Adjust Stock' : ''}
        onAction={canAdjust ? () => setDialogOpen(true) : undefined}
      />

      {error ? <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert> : null}

      <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: { xs: '1fr', md: canAdjust ? '2fr 1fr' : '1fr' }, mb: 2 }}>
        <SearchInput value={search} onChange={setSearch} placeholder="Search inventory..." />
        {canAdjust ? (
          <TextField select label="Category" value={categoryFilter} onChange={(e) => setCategoryFilter(e.target.value)}>
            <MenuItem value="">All categories</MenuItem>
            {categories.map((category) => (
              <MenuItem key={category.id} value={category.id}>{category.name}</MenuItem>
            ))}
          </TextField>
        ) : null}
      </Box>

      <DataTable
        rows={inventory}
        columns={[
          { key: 'product', label: 'Product', render: (row) => row.product?.name },
          { key: 'sku', label: 'SKU', render: (row) => row.product?.sku },
          { key: 'category', label: 'Category', render: (row) => row.product?.category_name },
          { key: 'current_stock', label: 'Current Stock' },
          { key: 'minimum_stock', label: 'Minimum Stock', render: (row) => row.product?.minimum_stock },
          { key: 'low_stock', label: 'Stock Level', render: (row) => <StatusChip active={!row.low_stock} /> },
        ]}
        onEdit={canAdjust ? openAdjustment : undefined}
        emptyText={loading ? 'Loading inventory...' : 'No inventory found.'}
      />

      {canAdjust ? (
        <Box sx={{ mt: 3, color: '#fff' }}>
          <PageHeader title="Inventory History" description={`Low stock items: ${lowStockCount}`} />
          <DataTable
            rows={transactions}
            columns={[
              { key: 'created_at', label: 'Time' },
              { key: 'product_sku', label: 'SKU' },
              { key: 'transaction_type', label: 'Type' },
              { key: 'quantity', label: 'Qty' },
              { key: 'previous_stock', label: 'Before' },
              { key: 'new_stock', label: 'After' },
              { key: 'reason', label: 'Reason' },
            ]}
            emptyText="No stock transactions yet."
          />
        </Box>
      ) : null}

      {canAdjust ? (
        <EntityDialog
          open={dialogOpen}
          title="Adjust Stock"
          onClose={() => setDialogOpen(false)}
          onSubmit={handleAdjustmentSubmit}
          submitting={submitting}
        >
          <TextField
            select
            label="Product"
            value={adjustment.product_id}
            onChange={(e) => setAdjustment({ ...adjustment, product_id: e.target.value })}
            required
          >
            <MenuItem value="">Select product</MenuItem>
            {products.map((product) => (
              <MenuItem key={product.id} value={product.id}>
                {product.name} ({product.sku})
              </MenuItem>
            ))}
          </TextField>
          <TextField
            label="Quantity"
            type="number"
            value={adjustment.quantity}
            onChange={(e) => setAdjustment({ ...adjustment, quantity: e.target.value })}
            required
          />
          <TextField
            select
            label="Direction"
            value={adjustment.direction}
            onChange={(e) => setAdjustment({ ...adjustment, direction: e.target.value })}
          >
            <MenuItem value="ADJUSTMENT_IN">Adjustment In</MenuItem>
            <MenuItem value="ADJUSTMENT_OUT">Adjustment Out</MenuItem>
          </TextField>
          <TextField
            multiline
            minRows={3}
            label="Reason"
            value={adjustment.reason}
            onChange={(e) => setAdjustment({ ...adjustment, reason: e.target.value })}
          />
        </EntityDialog>
      ) : null}
    </Box>
  )
}
