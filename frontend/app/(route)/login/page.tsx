import LoginForm from '@/app/(route)/login/_components/LoginForm'
import LoginSubMenu from '@/app/(route)/login/_components/LoginSubMenu'
import SocialLoginMenu from '@/app/(route)/login/_components/SocialLoginMenu'
import React from 'react'
import style from './loginPage.module.css'

function LoginPage() {
  return (
    <div className={style.main}>
      <LoginForm />
      <LoginSubMenu />
      <SocialLoginMenu />
    </div>
  )
}

export default LoginPage
