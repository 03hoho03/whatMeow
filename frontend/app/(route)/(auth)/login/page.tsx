import LoginForm from '@/app/(route)/(auth)/login/_components/LoginForm'
import LoginSubMenu from '@/app/(route)/(auth)/login/_components/LoginSubMenu'
import SocialLoginMenu from '@/app/(route)/(auth)/login/_components/SocialLoginMenu'
import React from 'react'
import style from './loginPage.module.css'
import PageBackLink from './_components/PageBackLink'

function LoginPage() {
  return (
    <div className={style.pageContainer}>
      <PageBackLink />
      <div className={style.formTitleContainer}>
        <h3>로그인</h3>
      </div>
      <LoginForm />
      <LoginSubMenu />
      <SocialLoginMenu />
    </div>
  )
}

export default LoginPage
