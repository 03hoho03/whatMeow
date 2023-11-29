'use client'
import React, { useEffect } from 'react'
import { useBodyScrollLock } from '@/app/_hooks/useBodyScrollLock'
import { useRecoilState } from 'recoil'
import loginModalState from '@/app/_store/atom/loginModalState'
import Modal from '../../../../../_common/Modal'
import ModalContent from '../ModalContent'

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
        <Modal>
          <ModalContent handleShowModal={handleShowModal} />
        </Modal>
      )}
    </>
  )
}

export default ModalTrigger
