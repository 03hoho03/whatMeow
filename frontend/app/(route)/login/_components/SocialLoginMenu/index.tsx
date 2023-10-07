import Link from 'next/link'
import React from 'react'
import { FcGoogle } from 'react-icons/fc'
import { RiKakaoTalkFill } from 'react-icons/ri'
import cn from 'classnames'
import style from './socialLoginMenu.module.css'

function SocialLoginMenu() {
  return (
    <div className={style.main}>
      <button
        type="button"
        className={cn(style.social_login_btn, { [style.kakao]: true })}
      >
        <Link href="/" className={style.logo_container}>
          <RiKakaoTalkFill className={style.kakao_logo} />
        </Link>
      </button>
      <button
        type="button"
        className={cn(style.social_login_btn, { [style.google]: true })}
      >
        <Link href="/" className={style.logo_container}>
          <FcGoogle className={style.google_logo} />
        </Link>
      </button>
    </div>
  )
}

export default SocialLoginMenu
