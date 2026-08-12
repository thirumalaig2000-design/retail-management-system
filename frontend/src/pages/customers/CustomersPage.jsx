import { useEffect, useState } from 'react'
import { Alert, Box, TextField } from '@mui/material'
import PageHeader from '../../components/common/PageHeader'
import SearchInput from '../../components/common/SearchInput'
import DataTable from '../../components/common/DataTable'
import EntityDialog from '../../components/common/EntityDialog'
import StatusChip from '../../components/common/StatusChip'
import { useAuth } from '../../context/AuthContext'
import { ROLES } from '../../constants/roles'
import { customerService } from '../../services/customerService'

const emptyForm = { name: '', phone: '', email: '', address: '', is_active: true }

export default function CustomersPage() {
  const { user } = useAuth()
  const [items, setItems] = useState([])
  const [search, setSearch] = useState('')
  const [error, setError] = useState('')
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editing, setEditing] = useState(null)
  const [form, setForm] = useState(emptyForm)
  const [submitting, setSubmitting] = useState(false)

  async function loadData() {
    try {
      const response = await customerService.list({ search })
      setItems(response.results || [])
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load customers.')
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
        await customerService.update(editing.id, form)
      } else {
        await customerService.create(form)
      }
      setDialogOpen(false)
      loadData()
    } catch (err) {
      setError(err.response?.data?.detail || 'Unable to save customer.')
    } finally {
      setSubmitting(false)
    }
  }

  async function handleDelete(item) {
    if (!window.confirm(`Delete ${item.name}?`)) return
    await customerService.remove(item.id)
    loadData()
  }

  return (
    <Box>
      <PageHeader
        title="Customers"
        description="Create and search customer records for sales."
        actionLabel="Add Customer"
        onAction={openCreate}
      />
      {error ? <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert> : null}
      <SearchInput value={search} onChange={setSearch} placeholder="Search customers..." />
      <DataTable
        rows={items}
        columns={[
          { key: 'name', label: 'Customer' },
          { key: 'phone', label: 'Phone' },
          { key: 'email', label: 'Email' },
          { key: 'address', label: 'Address' },
          { key: 'is_active', label: 'Status', render: (row) => <StatusChip active={row.is_active} /> },
        ]}
        onEdit={user?.role_code === ROLES.USER ? undefined : openEdit}
        onDelete={user?.role_code === ROLES.USER ? undefined : handleDelete}
      />
      <EntityDialog open={dialogOpen} title={editing ? 'Edit Customer' : 'Add Customer'} onClose={() => setDialogOpen(false)} onSubmit={handleSubmit} submitting={submitting}>
        <TextField label="Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
        <TextField label="Phone" value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
        <TextField label="Email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
        <TextField multiline minRows={3} label="Address" value={form.address} onChange={(e) => setForm({ ...form, address: e.target.value })} />
      </EntityDialog>
    </Box>
  )
}
