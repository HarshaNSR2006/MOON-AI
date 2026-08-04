import React, { useState } from 'react'
import Button from '@/components/ui/Button'

export default function CommandConsole() {
  const [lines, setLines] = useState<string[]>([])
  const [input, setInput] = useState('')

  function submit() {
    if (!input) return
    setLines((l) => [...l, `> ${input}`])
    // For now, push to UI. Integration with backend commands endpoint planned.
    setInput('')
  }

  return (
    <div className="p-4">
      <div className="border rounded p-3 h-64 overflow-auto bg-white dark:bg-slate-800">
        {lines.map((l, i) => (
          <div key={i} className="text-sm font-mono">{l}</div>
        ))}
      </div>
      <div className="mt-2 flex gap-2">
        <input value={input} onChange={(e) => setInput(e.target.value)} className="flex-1 border rounded px-3 py-2 font-mono" />
        <Button onClick={submit}>Run</Button>
      </div>
    </div>
  )
}
