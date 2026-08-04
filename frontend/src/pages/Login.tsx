import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Button from '@/components/ui/Button'
import { login } from '@/services/auth'
import { useAuth } from '@/store/useAuth'

export default function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const setToken = useAuth((s) => s.setToken)
  const navigate = useNavigate()

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    try {
      const data = await login({ username, password })
      const token = data.access_token || data.token || null
      if (!token) throw new Error('No token returned')
      setToken(token)
      navigate('/')
    } catch (err: any) {
      setError(err?.response?.data?.detail || err?.message || 'Login failed')
    }
  }

  return (
    <div className="max-w-md mx-auto p-6">
      <h2 className="text-xl font-semibold mb-4">Sign in</h2>
      <form onSubmit={handleSubmit} className="space-y-3">
        <div>
          <label className="block text-sm">Username</label>
          <input value={username} onChange={(e) => setUsername(e.target.value)} className="w-full border rounded px-3 py-2" />
        </div>
        <div>
          <label className="block text-sm">Password</label>
          <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" className="w-full border rounded px-3 py-2" />
        </div>
        {error && <div className="text-sm text-red-600">{error}</div>}
        <div>
          <Button type="submit">Sign in</Button>
        </div>
      </form>
    </div>
  )
}
