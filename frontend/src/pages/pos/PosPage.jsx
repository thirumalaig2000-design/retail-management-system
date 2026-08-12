import { useEffect, useMemo, useState } from 'react'
import { Alert, Box, Button, MenuItem, Stack, TextField, Typography } from '@mui/material'
import PageHeader from '../../components/common/PageHeader'
import SearchInput from '../../components/common/SearchInput'
import DataTable from '../../components/common/DataTable'
import { useAuth } from '../../context/AuthContext'
import { customerService } from '../../services/customerService'
import { productService } from '../../services/productService'
import { salesService } from '../../services/salesService'
import { ROLES } from '../../constants/roles'

const emptyCartItem = (product, quantity = 1) => ({
  product: product.id,
  name: product.name,
  sku: product.sku,
  quantity,
  unit_price: product.selling_price,
  discount: '0.00',
})

export default function PosPage() {
  const { user } = useAuth()
  const [search, setSearch] = useState('')
  const [products, setProducts] = useState([])
  const [customers, setCustomers] = useState([])
  const [customer, setCustomer] = useState('')
  const [cart, setCart] = useState([])
  const [discount, setDiscount] = useState('0.00')
  const [paymentMethod, setPaymentMethod] = useState('CASH')
  const [transactionReference, setTransactionReference] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(false)
  const [submitting, setSubmitting] = useState(false)

  async function loadData() {
    setLoading(true)
    setError('')
    try {
      const [productResponse, customerResponse] = await Promise.all([
        productService.list({ search, status: 'active' }),
        customerService.list({ status: 'active' }),
      ])
      setProducts(productResponse.results || [])
      setCustomers(customerResponse.results || [])
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load POS data.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData()
  }, [search])

  const cartTotals = useMemo(() => {
    const subtotal = cart.reduce((sum, item) => sum + Number(item.unit_price) * Number(item.quantity), 0)
    const grandDiscount = Number(discount || 0)
    const tax = 0
    const total = Math.max(0, subtotal - grandDiscount + tax)
    return {
      subtotal: subtotal.toFixed(2),
      total: total.toFixed(2),
    }
  }, [cart, discount])

  function addToCart(product) {
    setSuccess('')
    setCart((current) => {
      const existing = current.find((item) => item.product === product.id)
      if (existing) {
        return current.map((item) =>
          item.product === product.id
            ? { ...item, quantity: Number(item.quantity) + 1 }
            : item,
        )
      }
      return [...current, emptyCartItem(product)]
    })
  }

  function updateCartItem(index, patch) {
    setCart((current) => current.map((item, itemIndex) => (itemIndex === index ? { ...item, ...patch } : item)))
  }

  function removeCartItem(index) {
    setCart((current) => current.filter((_, itemIndex) => itemIndex !== index))
  }

  async function handleCheckout() {
    if (cart.length === 0) return
    setSubmitting(true)
    setError('')
    setSuccess('')
    try {
      const salePayload = {
        customer: customer || null,
        discount,
        items: cart.map((item) => ({
          product: item.product,
          quantity: item.quantity,
          unit_price: item.unit_price,
          discount: item.discount,
        })),
      }
      const sale = await salesService.create(salePayload)
      const completed = await salesService.complete(sale.id, {
        payment_method: paymentMethod,
        transaction_reference: transactionReference,
      })
      setCart([])
      setDiscount('0.00')
      setTransactionReference('')
      setSuccess(`Sale ${completed.sale_number} completed successfully.`)
    } catch (err) {
      setError(err.response?.data?.detail || 'Unable to complete sale.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <Box>
      <PageHeader
        title="POS"
        description="Search products, build a cart, and complete a sale."
        actionLabel={user?.role_code === ROLES.USER ? '' : undefined}
      />

      {error ? <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert> : null}
      {success ? <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert> : null}

      <SearchInput value={search} onChange={setSearch} placeholder="Search products for POS..." />

      <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', xl: '1.15fr 0.85fr' }, gap: 3 }}>
        <Box>
          <DataTable
            rows={products}
            columns={[
              { key: 'name', label: 'Product' },
              { key: 'sku', label: 'SKU' },
              { key: 'category_name', label: 'Category' },
              { key: 'selling_price', label: 'Price' },
              { key: 'current_stock', label: 'Stock' },
            ]}
            onEdit={(row) => addToCart(row)}
            onDelete={undefined}
            onToggle={undefined}
            emptyText={loading ? 'Loading products...' : 'No products available.'}
          />
        </Box>

        <Box sx={{ p: 3, bgcolor: 'rgba(255,255,255,0.04)', borderRadius: 3, border: '1px solid rgba(255,255,255,0.08)' }}>
          <Typography variant="h5" sx={{ color: '#fff', fontWeight: 900, mb: 2 }}>
            Cart
          </Typography>

          <Stack spacing={2}>
            <TextField select label="Customer" value={customer} onChange={(e) => setCustomer(e.target.value)}>
              <MenuItem value="">Walk-in customer</MenuItem>
              {customers.map((item) => (
                <MenuItem key={item.id} value={item.id}>{item.name}</MenuItem>
              ))}
            </TextField>
            <TextField label="Discount" type="number" value={discount} onChange={(e) => setDiscount(e.target.value)} />
            <TextField select label="Payment Method" value={paymentMethod} onChange={(e) => setPaymentMethod(e.target.value)}>
              <MenuItem value="CASH">Cash</MenuItem>
              <MenuItem value="CARD">Card</MenuItem>
              <MenuItem value="UPI">UPI</MenuItem>
            </TextField>
            <TextField
              label="Transaction Reference"
              value={transactionReference}
              onChange={(e) => setTransactionReference(e.target.value)}
            />
          </Stack>

          <Box sx={{ mt: 3, display: 'grid', gap: 1 }}>
            {cart.map((item, index) => (
              <Box key={`${item.product}-${index}`} sx={{ p: 1.5, border: '1px solid rgba(255,255,255,0.08)', borderRadius: 2 }}>
                <Typography sx={{ color: '#fff', fontWeight: 700 }}>{item.name}</Typography>
                <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.65)' }}>{item.sku}</Typography>
                <Stack direction="row" spacing={1} sx={{ mt: 1 }}>
                  <TextField
                    label="Qty"
                    type="number"
                    size="small"
                    value={item.quantity}
                    onChange={(e) => updateCartItem(index, { quantity: e.target.value })}
                    sx={{ width: 100 }}
                  />
                  <TextField
                    label="Price"
                    type="number"
                    size="small"
                    value={item.unit_price}
                    onChange={(e) => updateCartItem(index, { unit_price: e.target.value })}
                    sx={{ width: 120 }}
                  />
                  <TextField
                    label="Disc"
                    type="number"
                    size="small"
                    value={item.discount}
                    onChange={(e) => updateCartItem(index, { discount: e.target.value })}
                    sx={{ width: 110 }}
                  />
                </Stack>
                <Box sx={{ mt: 1, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.75)' }}>
                    Line total: {(Number(item.unit_price) * Number(item.quantity)).toFixed(2)}
                  </Typography>
                  <Button size="small" color="error" onClick={() => removeCartItem(index)}>
                    Remove
                  </Button>
                </Box>
              </Box>
            ))}
          </Box>

          <Box sx={{ mt: 3, display: 'grid', gap: 1, color: '#fff' }}>
            <Typography>Subtotal: {cartTotals.subtotal}</Typography>
            <Typography>Discount: {Number(discount || 0).toFixed(2)}</Typography>
            <Typography variant="h6" sx={{ fontWeight: 900 }}>Total: {cartTotals.total}</Typography>
          </Box>

          <Button
            fullWidth
            size="large"
            variant="contained"
            sx={{ mt: 3 }}
            onClick={handleCheckout}
            disabled={submitting || cart.length === 0}
          >
            {submitting ? 'Completing Sale...' : 'Complete Sale'}
          </Button>
        </Box>
      </Box>
    </Box>
  )
}
