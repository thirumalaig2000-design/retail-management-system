import { useEffect, useState } from 'react'
import { Alert, Box, TextField } from '@mui/material'
import PageHeader from '../../components/common/PageHeader'
import SearchInput from '../../components/common/SearchInput'
import DataTable from '../../components/common/DataTable'
import EntityDialog from '../../components/common/EntityDialog'
import StatusChip from '../../components/common/StatusChip'
import { categoryService } from '../../services/categoryService'

const emptyForm = { name: '', description: '', is_active: true }

export default function CategoriesPage() {
  const [items, setItems] = useState([])
  const [search, setSearch] = useState('')
  const [error, setError] = useState('')
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editing, setEditing] = useState(null)
  const [form, setForm] = useState(emptyForm)
  const [submitting, setSubmitting] = useState(false)

  async function loadData() {
    try {
      const response = await categoryService.list({ search })
      setItems(response.results || [])
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load categories.')
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
    setForm({ name: item.name || '', description: item.description || '', is_active: item.is_active })
    setDialogOpen(true)
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setSubmitting(true)
    try {
      if (editing) {
        await categoryService.update(editing.id, form)
      } else {
        await categoryService.create(form)
      }
      setDialogOpen(false)
      loadData()
    } catch (err) {
      setError(err.response?.data?.detail || 'Unable to save category.')
    } finally {
      setSubmitting(false)
    }
  }

  async function handleDelete(item) {
    if (!window.confirm(`Delete ${item.name}?`)) return
    await categoryService.remove(item.id)
    loadData()
  }

  async function handleToggle(item) {
    await (item.is_active ? categoryService.deactivate(item.id) : categoryService.activate(item.id))
    loadData()
  }

  return (
    <Box>
      <PageHeader title="Categories" description="Organize products into searchable groups." actionLabel="Add Category" onAction={openCreate} />
      {error ? <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert> : null}
      <SearchInput value={search} onChange={setSearch} placeholder="Search categories..." />
      <DataTable
        rows={items}
        columns={[
          { key: 'name', label: 'Category' },
          { key: 'description', label: 'Description' },
          { key: 'is_active', label: 'Status', render: (row) => <StatusChip active={row.is_active} /> },
        ]}
        onEdit={openEdit}
        onDelete={handleDelete}
        onToggle={handleToggle}
      />
      <EntityDialog open={dialogOpen} title={editing ? 'Edit Category' : 'Add Category'} onClose={() => setDialogOpen(false)} onSubmit={handleSubmit} submitting={submitting}>
        <TextField label="Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
        <TextField multiline minRows={3} label="Description" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
      </EntityDialog>
    </Box>
  )
}
