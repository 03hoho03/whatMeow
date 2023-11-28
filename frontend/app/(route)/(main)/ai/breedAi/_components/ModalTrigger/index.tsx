'use client'
import React, { useEffect } from 'react'
import LoginModal from '../LoginModal'
import { useBodyScrollLock } from '@/app/_hooks/useBodyScrollLock'
import LoginModalContent from '@/app/_common/LoginModalContent'
import { useRecoilState } from 'recoil'
import loginModalState from '@/app/_store/atom/loginModalState'

const ModalTrigger = () => {
  const [showModal, setShowModal] = useRecoilState<boolean>(loginModalState)
  const { lockScroll, openScroll } = useBodyScrollLock()

  useEffect(() => {
    if (showModal) {
      lockScroll()
    } else {
      openScroll()
    }
    return () => openScroll()
  }, [showModal])

  const handleShowModal = () => setShowModal((prev) => !prev)

  return (
    <>
      {showModal && (
        <LoginModal handleShowModal={handleShowModal}>
          <LoginModalContent />
        </LoginModal>
      )}
    </>
  )
}

export default ModalTrigger
