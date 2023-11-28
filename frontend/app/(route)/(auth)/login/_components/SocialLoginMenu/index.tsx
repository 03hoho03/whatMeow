import React from 'react'
import style from './socialLoginMenu.module.css'
import SocialLoginBtn from '../SocialLoginBtn'

function SocialLoginMenu() {
  const buttonInfo = [{ type: 'kakao' }, { type: 'google' }]
  return (
    <div className={style.main_wrapper}>
      {buttonInfo.map(({ type }, idx) => (
        <SocialLoginBtn key={`${type}-${idx}`} type={type} />
      ))}
    </div>
  )
}

export default SocialLoginMenu
