import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import { App } from './ui/App'

// Ask the browser not to evict IndexedDB under storage pressure. Silently ignored where unsupported.
void navigator.storage?.persist?.().catch(() => undefined)

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
