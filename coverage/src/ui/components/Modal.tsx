import { useEffect, useId, useRef, type ReactNode } from 'react'

interface ModalProps {
  title: string
  onClose: () => void
  children: ReactNode
  footer?: ReactNode
  size?: 'md' | 'lg'
}

/** Accessible modal: labelled, closes on Escape or backdrop click, keeps focus inside, restores focus on close. */
export function Modal({ title, onClose, children, footer, size = 'md' }: ModalProps) {
  const titleId = useId()
  const panel = useRef<HTMLDivElement>(null)
  const onCloseRef = useRef(onClose)
  useEffect(() => {
    onCloseRef.current = onClose
  })

  useEffect(() => {
    const previous = document.activeElement as HTMLElement | null
    const first = panel.current?.querySelector<HTMLElement>('input, select, textarea, button:not([data-close])')
    first?.focus()
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        e.stopPropagation()
        onCloseRef.current()
      }
      if (e.key === 'Tab' && panel.current) {
        const focusable = [...panel.current.querySelectorAll<HTMLElement>('input, select, textarea, button, a[href]')].filter((el) => !el.hasAttribute('disabled'))
        const [head, tail] = [focusable[0], focusable[focusable.length - 1]]
        if (e.shiftKey && document.activeElement === head) {
          e.preventDefault()
          tail?.focus()
        } else if (!e.shiftKey && document.activeElement === tail) {
          e.preventDefault()
          head?.focus()
        }
      }
    }
    document.addEventListener('keydown', onKey)
    return () => {
      document.removeEventListener('keydown', onKey)
      previous?.focus()
    }
  }, [])

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto bg-slate-900/40 p-4 sm:p-8" onMouseDown={(e) => e.target === e.currentTarget && onClose()}>
      <div
        ref={panel}
        role="dialog"
        aria-modal="true"
        aria-labelledby={titleId}
        className={`card w-full ${size === 'lg' ? 'max-w-3xl' : 'max-w-lg'} my-auto`}
      >
        <div className="flex items-center justify-between border-b border-slate-200 px-5 py-3">
          <h2 id={titleId} className="text-base font-semibold">
            {title}
          </h2>
          <button type="button" data-close className="btn btn-ghost btn-sm" onClick={onClose} aria-label="Close">
            ✕
          </button>
        </div>
        <div className="px-5 py-4">{children}</div>
        {footer && <div className="flex justify-end gap-2 border-t border-slate-200 px-5 py-3">{footer}</div>}
      </div>
    </div>
  )
}
