'use client'
import React from 'react'
import style from './modalContent.module.css'
import { useRouter } from 'next/navigation'
import { useSetRecoilState } from 'recoil'
import loginModalState from '@/app/_store/atom/loginModalState'

const ModalContent = () => {
  const router = useRouter()
  const setLoginModal = useSetRecoilState(loginModalState)

  const handleLoginLink = () => {
    setLoginModal(false)
    router.push('/login')
  }

  return (
    <div>
      <div className={style.modalContentContainer}>
        <div className={style.headerTitle}>
          <h5>로그인이 필요합니다</h5>
        </div>
        <div className={style.modalContent}>
          <p>로그인이 필요한 서비스 입니다.</p>
        </div>
      </div>
      <button
        type="button"
        onClick={handleLoginLink}
        className={style.confirmBtn}
      >
        로그인 하러가기
      </button>
    </div>
  )
}

export default ModalContent
