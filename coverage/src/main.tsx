import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import { ensureDefaultScenarios } from './db/repo'
import { App } from './ui/App'

// Ask the browser not to evict IndexedDB under storage pressure. Silently ignored where unsupported.
void navigator.storage?.persist?.().catch(() => undefined)

void ensureDefaultScenarios().catch((e) => console.error('Could not seed default scenarios', e))

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
