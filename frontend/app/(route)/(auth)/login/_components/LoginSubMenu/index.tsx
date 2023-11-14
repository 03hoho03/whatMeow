import Link from 'next/link'
import React from 'react'
import style from './loginSubMenu.module.css'

function LoginSubMenu() {
  return (
    <ul className={style.main}>
      <li className={style.subMenu_item}>
        <Link href="/join">회원가입</Link>
      </li>
      <li className={style.subMenu_separator}></li>
      <li>
        <Link href="/">아이디 찾기</Link>
      </li>
      <li className={style.subMenu_separator}></li>
      <li>
        <Link href="/">비밀번호 찾기</Link>
      </li>
    </ul>
  )
}

export default LoginSubMenu
