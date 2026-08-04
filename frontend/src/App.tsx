import React from 'react'
import { Routes, Route } from 'react-router-dom'
import MainLayout from './layouts/MainLayout'
import Home from './pages/Home'
import Login from './pages/Login'
import Chat from './pages/Chat'
import ConsolePage from './pages/Console'
import Automation from './pages/Automation'
import Plugins from './pages/Plugins'
import Memory from './pages/Memory'
import Files from './pages/Files'
import Settings from './pages/Settings'

export default function App() {
  return (
    <MainLayout>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/console" element={<ConsolePage />} />
        <Route path="/automation" element={<Automation />} />
        <Route path="/plugins" element={<Plugins />} />
        <Route path="/memory" element={<Memory />} />
        <Route path="/files" element={<Files />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </MainLayout>
  )
}
