import api from './api'

export interface LoginPayload {
  username: string
  password: string
}

export async function login(payload: LoginPayload) {
  const resp = await api.post('/auth/login', payload)
  return resp.data
}

export async function register(payload: { username: string; email?: string; password: string }) {
  const resp = await api.post('/auth/register', payload)
  return resp.data
}
