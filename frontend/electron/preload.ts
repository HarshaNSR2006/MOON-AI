import { contextBridge } from 'electron'

contextBridge.exposeInMainWorld('moon', {
  ping: () => 'pong',
})
