import create from 'zustand'

interface AuthState {
  token: string | null
  setToken: (t: string | null) => void
}

export const useAuth = create<AuthState>((set) => ({
  token: typeof window !== 'undefined' ? localStorage.getItem('moon_token') : null,
  setToken: (t) => {
    try {
      if (t) localStorage.setItem('moon_token', t)
      else localStorage.removeItem('moon_token')
    } catch (e) {
      // ignore
    }
    set({ token: t })
  },
}))
