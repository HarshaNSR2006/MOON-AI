import React from 'react'

export default function Modal({ open, onClose, children }: { open: boolean; onClose: () => void; children?: React.ReactNode }) {
  if (!open) return null
  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black/50 z-50">
      <div className="bg-white dark:bg-slate-800 rounded p-4 w-full max-w-2xl">
        <div className="flex justify-end">
          <button onClick={onClose} className="px-2 py-1">
            Close
          </button>
        </div>
        <div>{children}</div>
      </div>
    </div>
  )
}
