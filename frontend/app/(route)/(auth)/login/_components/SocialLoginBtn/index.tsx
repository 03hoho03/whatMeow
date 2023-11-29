'use client'

import React from 'react'
import cn from 'classnames'
import style from './socialLoginBtn.module.css'
import { RiKakaoTalkFill } from 'react-icons/ri'
import { FcGoogle } from 'react-icons/fc'
import { BASE_URL } from '@/app/_utils/constants'

interface SocialProps {
  type: string
}
const SocialLoginBtn = ({ type }: SocialProps) => {
  return (
    <form
      method="GET"
      action={`${BASE_URL}/api/v1/auth/${type}`}
      className={style.social_form}
    >
      <button
        type="submit"
        className={cn(style.social_login_btn, { [style[type]]: true })}
      >
        {type === 'kakao' ? (
          <RiKakaoTalkFill className={style.kakao_logo} />
        ) : type === 'google' ? (
          <FcGoogle className={style.google_logo} />
        ) : (
          <></>
        )}
      </button>
    </form>
  )
}

export default SocialLoginBtn
