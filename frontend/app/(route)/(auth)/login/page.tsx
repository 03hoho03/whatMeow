import LoginForm from '@/app/(route)/(auth)/login/_components/LoginForm'
import LoginSubMenu from '@/app/(route)/(auth)/login/_components/LoginSubMenu'
import SocialLoginMenu from '@/app/(route)/(auth)/login/_components/SocialLoginMenu'
import React from 'react'
import style from './loginPage.module.css'

function LoginPage() {
  return (
    <div className={style.main}>
      <div>
        <h3>로그인</h3>
      </div>
      <LoginForm />
      <LoginSubMenu />
      <SocialLoginMenu />
    </div>
  )
}

export default LoginPage
