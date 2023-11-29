'use client'
import React from 'react'
import style from './modal.module.css'

const Modal = ({
  children,
  handleShowModal,
}: {
  children: React.ReactNode
  handleShowModal?: () => void
}) => {
  return (
    <div className={style.modalOverlay} onClick={handleShowModal}>
      <div className={style.modal} onClick={(e) => e.stopPropagation()}>
        {children}
      </div>
    </div>
  )
}

export default Modal
