import React, { useEffect, useState } from 'react'
import { wsClient } from '@/services/ws'
import { useAuth } from '@/store/useAuth'
import Button from '@/components/ui/Button'

export default function Chat() {
  const [messages, setMessages] = useState<any[]>([])
  const [input, setInput] = useState('')
  const token = useAuth((s) => s.token)

  useEffect(() => {
    wsClient.connect('/ws/chat', token || undefined)
    const unsub = wsClient.onMessage((data) => {
      setMessages((m) => [...m, data])
    })
    return () => {
      unsub()
      wsClient.close()
    }
  }, [token])

  function send() {
    if (!input) return
    wsClient.send({ type: 'user_message', text: input })
    setMessages((m) => [...m, { type: 'outgoing', text: input }])
    setInput('')
  }

  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold">Chat</h2>
      <div className="mt-4 border rounded p-4 h-[60vh] overflow-auto bg-white dark:bg-slate-800">
        {messages.map((msg, idx) => (
          <div key={idx} className={`mb-2 ${msg.type === 'outgoing' ? 'text-right' : 'text-left'}`}>
            <div className="inline-block rounded px-3 py-2 bg-slate-100 dark:bg-slate-700">{msg.text || JSON.stringify(msg)}</div>
          </div>
        ))}
      </div>
      <div className="mt-3 flex gap-2">
        <input value={input} onChange={(e) => setInput(e.target.value)} className="flex-1 border rounded px-3 py-2" />
        <Button onClick={send}>Send</Button>
      </div>
    </div>
  )
}
