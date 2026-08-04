import React from 'react'
import Button from '@/components/ui/Button'

export default function Home() {
  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold">Dashboard</h2>
      <p className="mt-2 text-sm">This is the initial dashboard for MOON AI.</p>
      <div className="mt-4">
        <Button>Get Started</Button>
      </div>
    </div>
  )
}
