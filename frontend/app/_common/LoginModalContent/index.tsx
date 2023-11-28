'use client'
import React from 'react'
import style from './loginModalContent.module.css'
import { useRouter } from 'next/navigation'
import { useSetRecoilState } from 'recoil'
import loginModalState from '@/app/_store/atom/loginModalState'

const LoginModalContent = () => {
  const router = useRouter()
  const setLoginModal = useSetRecoilState(loginModalState)
  const HandleClickLoginBtn = () => {
    setLoginModal(false)
    router.push('/login')
  }

  return (
    <section className={style.ContentContainer}>
      <header className={style.modalContentHeader}>
        로그인이 필요한 서비스에요 !
      </header>
      <div className={style.modalContent}>
        간단하게 로그인 후 다양한 서비스를 이용해 보세요.
      </div>
      <button
        onClick={HandleClickLoginBtn}
        type="button"
        className={style.linkBtn}
      >
        로그인
      </button>
    </section>
  )
}

export default LoginModalContent
