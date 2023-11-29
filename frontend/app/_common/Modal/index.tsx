'use client'
import React, { MouseEventHandler, useCallback, useEffect, useRef } from 'react'
import style from './modal.module.css'
import { useRouter } from 'next/navigation'
import { useBodyScrollLock } from '@/app/_hooks/useBodyScrollLock'

interface ModalProps {
  children: React.ReactNode
}

const Modal = ({ children }: ModalProps) => {
  const router = useRouter()
  const overlay = useRef(null)
  const wrapper = useRef(null)
  const { openScroll, lockScroll } = useBodyScrollLock()

  const onDismiss = useCallback(() => {
    router.back()
  }, [router])

  const onClick: MouseEventHandler = useCallback(
    (e) => {
      if (e.target === overlay.current || e.target === wrapper.current) {
        if (onDismiss) onDismiss()
      }
    },
    [onDismiss, overlay, wrapper],
  )

  const onKeyDown = useCallback(
    (e: KeyboardEvent) => {
      if (e.key === 'Escape') onDismiss()
    },
    [onDismiss],
  )

  useEffect(() => {
    document.addEventListener('keydown', onKeyDown)
    return () => document.removeEventListener('keydown', onKeyDown)
  }, [onKeyDown])

  useEffect(() => {
    lockScroll()

    return () => {
      openScroll()
    }
  }, [])

  return (
    <div ref={overlay} className={style.modalOverlay} onClick={onClick}>
      <div ref={wrapper} className={style.modal}>
        {children}
      </div>
    </div>
  )
}

export default Modal
