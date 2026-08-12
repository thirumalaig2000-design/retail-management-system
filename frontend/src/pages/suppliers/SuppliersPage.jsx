import { useEffect, useState } from 'react'
import { Alert, Box, TextField } from '@mui/material'
import PageHeader from '../../components/common/PageHeader'
import SearchInput from '../../components/common/SearchInput'
import DataTable from '../../components/common/DataTable'
import EntityDialog from '../../components/common/EntityDialog'
import StatusChip from '../../components/common/StatusChip'
import { supplierService } from '../../services/supplierService'

const emptyForm = {
  name: '',
  contact_person: '',
  phone: '',
  email: '',
  address: '',
  tax_number: '',
  is_active: true,
}

export default function SuppliersPage() {
  const [items, setItems] = useState([])
  const [search, setSearch] = useState('')
  const [error, setError] = useState('')
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editing, setEditing] = useState(null)
  const [form, setForm] = useState(emptyForm)
  const [submitting, setSubmitting] = useState(false)

  async function loadData() {
    try {
      const response = await supplierService.list({ search })
      setItems(response.results || [])
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load suppliers.')
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
    setForm(item)
    setDialogOpen(true)
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setSubmitting(true)
    try {
      if (editing) {
        await supplierService.update(editing.id, form)
      } else {
        await supplierService.create(form)
      }
      setDialogOpen(false)
      loadData()
    } catch (err) {
      setError(err.response?.data?.detail || 'Unable to save supplier.')
    } finally {
      setSubmitting(false)
    }
  }

  async function handleDelete(item) {
    if (!window.confirm(`Delete ${item.name}?`)) return
    await supplierService.remove(item.id)
    loadData()
  }

  return (
    <Box>
      <PageHeader title="Suppliers" description="Maintain supplier contacts and reference data." actionLabel="Add Supplier" onAction={openCreate} />
      {error ? <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert> : null}
      <SearchInput value={search} onChange={setSearch} placeholder="Search suppliers..." />
      <DataTable
        rows={items}
        columns={[
          { key: 'name', label: 'Supplier' },
          { key: 'contact_person', label: 'Contact Person' },
          { key: 'phone', label: 'Phone' },
          { key: 'email', label: 'Email' },
          { key: 'is_active', label: 'Status', render: (row) => <StatusChip active={row.is_active} /> },
        ]}
        onEdit={openEdit}
        onDelete={handleDelete}
      />
      <EntityDialog open={dialogOpen} title={editing ? 'Edit Supplier' : 'Add Supplier'} onClose={() => setDialogOpen(false)} onSubmit={handleSubmit} submitting={submitting}>
        <TextField label="Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
        <TextField label="Contact Person" value={form.contact_person} onChange={(e) => setForm({ ...form, contact_person: e.target.value })} />
        <TextField label="Phone" value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
        <TextField label="Email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
        <TextField label="Tax Number" value={form.tax_number} onChange={(e) => setForm({ ...form, tax_number: e.target.value })} />
        <TextField multiline minRows={3} label="Address" value={form.address} onChange={(e) => setForm({ ...form, address: e.target.value })} />
      </EntityDialog>
    </Box>
  )
}
