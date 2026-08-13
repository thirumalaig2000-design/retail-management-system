import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { fetchProfile, login as loginRequest, logout as logoutRequest } from '../services/authService'
import { storage } from '../services/storage'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => storage.getUser())
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    let mounted = true

    async function bootstrap() {
      const accessToken = storage.getAccessToken()
      const refreshToken = storage.getRefreshToken()
      const cachedUser = storage.getUser()

      if (!accessToken || !refreshToken || !cachedUser) {
        if (mounted) {
          setUser(null)
          setIsLoading(false)
        }
        return
      }

      try {
        const profile = await fetchProfile()
        const sessionUser = { ...cachedUser, ...profile }
        storage.setSession({
          access: accessToken,
          refresh: refreshToken,
          user: sessionUser,
        })
        if (mounted) {
          setUser(sessionUser)
        }
      } catch {
        storage.clearSession()
        if (mounted) {
          setUser(null)
        }
      } finally {
        if (mounted) {
          setIsLoading(false)
        }
      }
    }

    bootstrap()
    return () => {
      mounted = false
    }
  }, [])

  useEffect(() => {
    const handleAuthExpired = () => {
      setUser(null)
    }

    window.addEventListener('smartstock:auth-expired', handleAuthExpired)
    return () => window.removeEventListener('smartstock:auth-expired', handleAuthExpired)
  }, [])

  const value = useMemo(
    () => ({
      user,
      isAuthenticated: Boolean(user),
      isLoading,
      async login(email, password) {
        const session = await loginRequest(email, password)
        setUser(session.user)
        return session
      },
      async logout() {
        try {
          await logoutRequest()
        } catch {
          // The session may already be expired or the network may be unavailable.
          // Local logout should still succeed in either case.
        } finally {
          // A failed or expired refresh token must not leave the user signed in
          // on this device. The server call is best-effort token blacklisting;
          // clearing the local session is required for the UI logout flow.
          storage.clearSession()
          setUser(null)
        }
      },
      setUser,
    }),
    [isLoading, user],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
