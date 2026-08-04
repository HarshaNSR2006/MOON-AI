import React, { useEffect } from 'react'

export default function Toast({ message, onClose }: { message: string; onClose?: () => void }) {
  useEffect(() => {
    const id = setTimeout(() => onClose && onClose(), 4000)
    return () => clearTimeout(id)
  }, [])

  return (
    <div className="fixed bottom-6 right-6 bg-slate-900 text-white px-4 py-2 rounded shadow">{message}</div>
  )
}
