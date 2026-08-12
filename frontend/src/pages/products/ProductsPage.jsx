import { useEffect, useState } from 'react'
import { Alert, Box, MenuItem, TextField } from '@mui/material'
import PageHeader from '../../components/common/PageHeader'
import SearchInput from '../../components/common/SearchInput'
import DataTable from '../../components/common/DataTable'
import EntityDialog from '../../components/common/EntityDialog'
import StatusChip from '../../components/common/StatusChip'
import { useAuth } from '../../context/AuthContext'
import { ROLES } from '../../constants/roles'
import { productService } from '../../services/productService'
import { categoryService } from '../../services/categoryService'

const emptyForm = {
  name: '',
  sku: '',
  barcode: '',
  category: '',
  brand: '',
  description: '',
  purchase_price: '',
  selling_price: '',
  tax_percentage: '0',
  current_stock: '0',
  minimum_stock: '0',
  is_active: true,
}

export default function ProductsPage() {
  const { user } = useAuth()
  const [items, setItems] = useState([])
  const [categories, setCategories] = useState([])
  const [search, setSearch] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editing, setEditing] = useState(null)
  const [form, setForm] = useState(emptyForm)
  const [submitting, setSubmitting] = useState(false)

  async function loadData() {
    setLoading(true)
    setError('')
    try {
      const [productResponse, categoryResponse] = await Promise.all([
        productService.list({ search }),
        categoryService.list({ status: 'active' }),
      ])
      setItems(productResponse.results || [])
      setCategories(categoryResponse.results || [])
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load products.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData()
  }, [search])

  function openCreate() {
    setEditing(null)
    setForm(emptyForm)
    setDialogOpen(true)
  }

  function openEdit(item) {
    setEditing(item)
    setForm({
      name: item.name || '',
      sku: item.sku || '',
      barcode: item.barcode || '',
      category: item.category || '',
      brand: item.brand || '',
      description: item.description || '',
      purchase_price: item.purchase_price || '',
      selling_price: item.selling_price || '',
      tax_percentage: item.tax_percentage || '0',
      current_stock: item.current_stock || '0',
      minimum_stock: item.minimum_stock || '0',
      is_active: item.is_active,
    })
    setDialogOpen(true)
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setSubmitting(true)
    try {
      const payload = {
        ...form,
        category: Number(form.category),
        current_stock: Number(form.current_stock),
        minimum_stock: Number(form.minimum_stock),
      }
      if (editing) {
        await productService.update(editing.id, payload)
      } else {
        await productService.create(payload)
      }
      setDialogOpen(false)
      await loadData()
    } catch (err) {
      setError(err.response?.data?.detail || 'Unable to save product.')
    } finally {
      setSubmitting(false)
    }
  }

  async function handleDelete(item) {
    if (!window.confirm(`Delete ${item.name}?`)) return
    await productService.remove(item.id)
    loadData()
  }

  async function handleToggle(item) {
    await (item.is_active ? productService.deactivate(item.id) : productService.activate(item.id))
    loadData()
  }

  return (
    <Box>
      <PageHeader
        title="Products"
        description="Create, search, update, activate, and deactivate inventory products."
        actionLabel={user?.role_code === ROLES.USER ? '' : 'Add Product'}
        onAction={user?.role_code === ROLES.USER ? undefined : openCreate}
      />

      {error ? <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert> : null}
      <SearchInput value={search} onChange={setSearch} placeholder="Search products..." />

      <DataTable
        rows={items}
        columns={[
          { key: 'name', label: 'Product' },
          { key: 'sku', label: 'SKU' },
          { key: 'category_name', label: 'Category' },
          { key: 'brand', label: 'Brand' },
          { key: 'selling_price', label: 'Selling Price' },
          { key: 'current_stock', label: 'Stock' },
          { key: 'is_active', label: 'Status', render: (row) => <StatusChip active={row.is_active} /> },
        ]}
        onEdit={user?.role_code === ROLES.USER ? undefined : openEdit}
        onDelete={user?.role_code === ROLES.USER ? undefined : handleDelete}
        onToggle={user?.role_code === ROLES.USER ? undefined : handleToggle}
        emptyText={loading ? 'Loading products...' : 'No products found.'}
      />

      {user?.role_code === ROLES.USER ? null : (
        <EntityDialog
          open={dialogOpen}
          title={editing ? 'Edit Product' : 'Add Product'}
          onClose={() => setDialogOpen(false)}
          onSubmit={handleSubmit}
          submitting={submitting}
        >
          <TextField label="Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
          <TextField label="SKU" value={form.sku} onChange={(e) => setForm({ ...form, sku: e.target.value })} required />
          <TextField label="Barcode" value={form.barcode} onChange={(e) => setForm({ ...form, barcode: e.target.value })} />
          <TextField select label="Category" value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })} required>
            <MenuItem value="">Select category</MenuItem>
            {categories.map((category) => (
              <MenuItem key={category.id} value={category.id}>{category.name}</MenuItem>
            ))}
          </TextField>
          <TextField label="Brand" value={form.brand} onChange={(e) => setForm({ ...form, brand: e.target.value })} />
          <TextField multiline minRows={3} label="Description" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
          <TextField label="Purchase Price" type="number" value={form.purchase_price} onChange={(e) => setForm({ ...form, purchase_price: e.target.value })} required />
          <TextField label="Selling Price" type="number" value={form.selling_price} onChange={(e) => setForm({ ...form, selling_price: e.target.value })} required />
          <TextField label="Tax %" type="number" value={form.tax_percentage} onChange={(e) => setForm({ ...form, tax_percentage: e.target.value })} />
          <TextField label="Current Stock" type="number" value={form.current_stock} onChange={(e) => setForm({ ...form, current_stock: e.target.value })} />
          <TextField label="Minimum Stock" type="number" value={form.minimum_stock} onChange={(e) => setForm({ ...form, minimum_stock: e.target.value })} />
        </EntityDialog>
      )}
    </Box>
  )
}
