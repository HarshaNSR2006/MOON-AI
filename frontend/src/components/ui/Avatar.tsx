import React from 'react'

export default function Avatar({ name }: { name?: string }) {
  const initials = (name || 'U').split(' ').map((p) => p[0]).slice(0, 2).join('')
  return <div className="w-8 h-8 rounded-full bg-indigo-600 text-white flex items-center justify-center text-sm">{initials}</div>
}
