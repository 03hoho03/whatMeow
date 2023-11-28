'use client'

import React, { useEffect } from 'react'
import style from './modal.module.css'
// import cn from 'classnames'
import { useRouter } from 'next/navigation'
import { useBodyScrollLock } from '@/app/_hooks/useBodyScrollLock'

interface ModalProps {
  children: React.ReactNode
  visible: boolean
}

const Modal = ({ children, visible = false }: ModalProps) => {
  const router = useRouter()
  const { openScroll, lockScroll } = useBodyScrollLock()

  useEffect(() => {
    if (visible) {
      lockScroll()
    }
    return () => {
      openScroll()
    }
  }, [visible])

  // Modal 닫기 함수
  const closeModal = () => {
    router.back()
  }
  return (
    visible && (
      <div className={style.modalOverlay} onClick={closeModal}>
        <div className={style.modal} onClick={(e) => e.stopPropagation()}>
          {children}
        </div>
      </div>
    )
  )
}

export default Modal
