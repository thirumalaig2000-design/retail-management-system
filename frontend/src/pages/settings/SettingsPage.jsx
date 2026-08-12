import { useEffect, useMemo, useState } from 'react'
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Grid,
  Stack,
  Switch,
  TextField,
  Typography,
  FormControlLabel,
} from '@mui/material'
import PageHeader from '../../components/common/PageHeader'
import { getSecurityReview } from '../../services/auditService'
import { getSystemSettings, updateSystemSetting } from '../../services/settingsService'

export default function SettingsPage() {
  const [settings, setSettings] = useState(null)
  const [security, setSecurity] = useState(null)
  const [error, setError] = useState('')
  const [savingId, setSavingId] = useState(null)
  const [drafts, setDrafts] = useState({})

  useEffect(() => {
    let active = true
    Promise.all([getSystemSettings(), getSecurityReview()])
      .then(([settingsData, securityData]) => {
        if (!active) return
        setSettings(settingsData.results || [])
        setSecurity(securityData)
        setDrafts(
          Object.fromEntries(
            (settingsData.results || []).map((item) => [item.id, item.value ?? '']),
          ),
        )
      })
      .catch(() => {
        if (active) setError('Unable to load system settings right now.')
      })
    return () => {
      active = false
    }
  }, [])

  const groupedSettings = useMemo(() => {
    const groups = {}
    ;(settings || []).forEach((item) => {
      if (!groups[item.section]) groups[item.section] = []
      groups[item.section].push(item)
    })
    return groups
  }, [settings])

  const handleSave = async (setting) => {
    setSavingId(setting.id)
    try {
      const updated = await updateSystemSetting(setting.id, drafts[setting.id])
      setSettings((current) => current.map((item) => (item.id === updated.id ? updated : item)))
    } catch {
      setError(`Unable to save ${setting.label}.`)
    } finally {
      setSavingId(null)
    }
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>
  }

  if (!settings) {
    return (
      <Box sx={{ display: 'grid', placeItems: 'center', minHeight: 260 }}>
        <CircularProgress />
      </Box>
    )
  }

  return (
    <Box>
      <PageHeader
        title="System settings"
        description="Manage store configuration, document defaults, and inventory thresholds."
      />

      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} md={8}>
          <Card sx={panelSx}>
            <CardContent>
              <Typography variant="h6" sx={{ fontWeight: 800, mb: 1 }}>
                Security review
              </Typography>
              <Typography sx={{ color: 'rgba(255,255,255,0.7)', mb: 2 }}>
                This summary surfaces a few important configuration checks before production deployment.
              </Typography>
              <Stack spacing={1.5}>
                {(security?.checks || []).map((check) => (
                  <Box
                    key={check.name}
                    sx={{
                      display: 'flex',
                      gap: 2,
                      justifyContent: 'space-between',
                      alignItems: 'flex-start',
                      p: 1.5,
                      borderRadius: 2,
                      bgcolor: 'rgba(255,255,255,0.04)',
                      border: '1px solid rgba(255,255,255,0.08)',
                    }}
                  >
                    <Box>
                      <Typography fontWeight={700}>{check.name}</Typography>
                      <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.68)', mt: 0.5 }}>
                        {check.detail}
                      </Typography>
                    </Box>
                    <Chip
                      label={check.passed ? 'Pass' : 'Review'}
                      color={check.passed ? 'success' : 'warning'}
                      size="small"
                      variant={check.passed ? 'filled' : 'outlined'}
                    />
                  </Box>
                ))}
              </Stack>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card sx={panelSx}>
            <CardContent>
              <Typography variant="h6" sx={{ fontWeight: 800, mb: 1 }}>
                Notes
              </Typography>
              <Typography sx={{ color: 'rgba(255,255,255,0.72)' }}>
                Settings never store secrets. Audit logs capture every update here so the configuration history stays traceable.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {Object.entries(groupedSettings).map(([section, items]) => (
        <Card key={section} sx={{ ...panelSx, mb: 2 }}>
          <CardContent>
            <Typography variant="h6" sx={{ fontWeight: 800, mb: 2 }}>
              {section}
            </Typography>
            <Grid container spacing={2}>
              {items.map((setting) => (
                <Grid item xs={12} md={6} key={setting.id}>
                  <Box
                    sx={{
                      p: 2,
                      borderRadius: 3,
                      bgcolor: 'rgba(255,255,255,0.04)',
                      border: '1px solid rgba(255,255,255,0.08)',
                    }}
                  >
                    <Stack direction="row" justifyContent="space-between" spacing={2} sx={{ mb: 1 }}>
                      <Box>
                        <Typography fontWeight={700}>{setting.label}</Typography>
                        <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.68)' }}>
                          {setting.description || setting.key}
                        </Typography>
                      </Box>
                      <Chip
                        label={setting.value_type}
                        size="small"
                        variant="outlined"
                      />
                    </Stack>

                    {setting.value_type === 'BOOLEAN' ? (
                      <FormControlLabel
                        control={
                          <Switch
                            checked={String(drafts[setting.id]).toLowerCase() === 'true'}
                            onChange={(event) =>
                              setDrafts((current) => ({
                                ...current,
                                [setting.id]: event.target.checked ? 'true' : 'false',
                              }))
                            }
                          />
                        }
                        label={String(drafts[setting.id]).toLowerCase() === 'true' ? 'Enabled' : 'Disabled'}
                      />
                    ) : (
                      <TextField
                        value={drafts[setting.id] ?? ''}
                        onChange={(event) =>
                          setDrafts((current) => ({
                            ...current,
                            [setting.id]: event.target.value,
                          }))
                        }
                        fullWidth
                        multiline={setting.key.includes('address')}
                        minRows={setting.key.includes('address') ? 2 : 1}
                      />
                    )}

                    <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mt: 2 }}>
                      <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.56)' }}>
                        Updated {setting.updated_at ? new Date(setting.updated_at).toLocaleString() : 'recently'}
                      </Typography>
                      <Button
                        variant="contained"
                        onClick={() => handleSave(setting)}
                        disabled={savingId === setting.id || !setting.is_editable}
                      >
                        {savingId === setting.id ? 'Saving...' : 'Save'}
                      </Button>
                    </Stack>
                  </Box>
                </Grid>
              ))}
            </Grid>
          </CardContent>
        </Card>
      ))}
    </Box>
  )
}

const panelSx = {
  borderRadius: 4,
  bgcolor: 'rgba(255,255,255,0.06)',
  color: '#fff',
  border: '1px solid rgba(255,255,255,0.08)',
  backdropFilter: 'blur(14px)',
}
