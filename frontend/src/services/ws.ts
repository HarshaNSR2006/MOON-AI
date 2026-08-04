type MessageHandler = (data: any) => void

export class WebSocketClient {
  private ws: WebSocket | null = null
  private handlers: MessageHandler[] = []

  connect(path = '/ws/chat', token?: string) {
    const configuredBase = (import.meta.env.VITE_API_BASE as string | undefined)?.trim() || '/api'
    const query = token ? `?token=${encodeURIComponent(token)}` : ''

    let url: string
    if (configuredBase.startsWith('http')) {
      const wsProto = configuredBase.startsWith('https') ? 'wss' : 'ws'
      const host = new URL(configuredBase).host
      url = `${wsProto}://${host}${path}${query}`
    } else {
      const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws'
      url = `${protocol}://${window.location.host}${path}${query}`
    }

    this.ws = new WebSocket(url)
    this.ws.onopen = () => console.info('WS connected', url)
    this.ws.onmessage = (ev) => {
      try {
        const payload = JSON.parse(ev.data)
        this.handlers.forEach((h) => h(payload))
      } catch (e) {
        this.handlers.forEach((h) => h(ev.data))
      }
    }
    this.ws.onclose = () => console.info('WS closed')
    this.ws.onerror = (ev) => console.error('WS error', ev)
  }

  send(obj: any) {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) return false
    try {
      this.ws.send(typeof obj === 'string' ? obj : JSON.stringify(obj))
      return true
    } catch (e) {
      return false
    }
  }

  onMessage(handler: MessageHandler) {
    this.handlers.push(handler)
    return () => {
      this.handlers = this.handlers.filter((h) => h !== handler)
    }
  }

  close() {
    if (this.ws) this.ws.close()
    this.ws = null
  }
}

export const wsClient = new WebSocketClient()
