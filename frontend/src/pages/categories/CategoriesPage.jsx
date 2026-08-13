import { useEffect, useState } from 'react'
import { Formik } from 'formik'
import * as Yup from 'yup'
import { Alert, Box, TextField } from '@mui/material'
import PageHeader from '../../components/common/PageHeader'
import SearchInput from '../../components/common/SearchInput'
import DataTable from '../../components/common/DataTable'
import EntityDialog from '../../components/common/EntityDialog'
import StatusChip from '../../components/common/StatusChip'
import { categoryService } from '../../services/categoryService'
import FormikTextField from '../../components/common/FormikTextField'

const emptyForm = { name: '', description: '', is_active: true }
const categorySchema = Yup.object({ name: Yup.string().trim().max(100, 'Name must be 100 characters or fewer.').required('Name is required.'), description: Yup.string().max(500, 'Description must be 500 characters or fewer.') })

export default function CategoriesPage() {
  const [items, setItems] = useState([])
  const [search, setSearch] = useState('')
  const [error, setError] = useState('')
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editing, setEditing] = useState(null)
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
    setDialogOpen(true)
  }

  function openEdit(item) {
    setEditing(item)
    setDialogOpen(true)
  }

  async function handleSubmit(values) {
    setSubmitting(true)
    try {
      if (editing) {
        await categoryService.update(editing.id, values)
      } else {
        await categoryService.create(values)
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
      <Formik enableReinitialize initialValues={editing ? { name: editing.name || '', description: editing.description || '', is_active: editing.is_active } : emptyForm} validationSchema={categorySchema} onSubmit={handleSubmit}>
        {({ handleSubmit }) => (
          <EntityDialog open={dialogOpen} title={editing ? 'Edit Category' : 'Add Category'} onClose={() => setDialogOpen(false)} onSubmit={handleSubmit} submitting={submitting}>
            <FormikTextField name="name" label="Name" required />
            <FormikTextField name="description" multiline minRows={3} label="Description" />
          </EntityDialog>
        )}
      </Formik>
    </Box>
  )
}
