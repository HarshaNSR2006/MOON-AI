import React from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '@/store/useAuth'

const MainLayout: React.FC<{ children?: React.ReactNode }> = ({ children }) => {
  const token = useAuth((s) => s.token)
  const setToken = useAuth((s) => s.setToken)

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 text-slate-900 dark:text-slate-100">
      <header className="h-16 bg-white dark:bg-slate-800 shadow-sm flex items-center px-4 justify-between">
        <div className="font-bold">MOON AI</div>
        <nav className="flex items-center gap-3">
          <Link to="/">Dashboard</Link>
          <Link to="/chat">Chat</Link>
          <Link to="/console">Console</Link>
          <Link to="/automation">Automation</Link>
          {!token ? <Link to="/login">Sign in</Link> : <button onClick={() => setToken(null)}>Sign out</button>}
        </nav>
      </header>
      <div className="flex">
        <aside className="w-64 border-r border-slate-200 dark:border-slate-800 p-4">
          <nav className="flex flex-col gap-2">
            <Link to="/">Dashboard</Link>
            <Link to="/chat">Chat</Link>
            <Link to="/">Memory</Link>
            <Link to="/">Automation</Link>
            <Link to="/">Plugins</Link>
            <Link to="/">Files</Link>
            <Link to="/">Settings</Link>
          </nav>
        </aside>
        <div className="flex-1">{children}</div>
      </div>
      <footer className="h-10 bg-white dark:bg-slate-800 border-t text-sm flex items-center px-4">Status bar</footer>
    </div>
  )
}

export default MainLayout
