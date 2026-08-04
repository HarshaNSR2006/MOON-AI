type Subscriber = (msg: { title: string; body?: string }) => void

class NotificationService {
  subscribers: Subscriber[] = []

  subscribe(fn: Subscriber) {
    this.subscribers.push(fn)
    return () => (this.subscribers = this.subscribers.filter((s) => s !== fn))
  }

  notify(title: string, body?: string) {
    this.subscribers.forEach((s) => s({ title, body }))
  }
}

export const notifications = new NotificationService()
