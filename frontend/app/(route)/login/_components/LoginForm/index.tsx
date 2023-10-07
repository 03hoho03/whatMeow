'use client'

import React, { useState } from 'react'
import style from './loginForm.module.css'

function LoginForm() {
  const [email, setEmail] = useState<string>('')
  const [password, setPassword] = useState<string>('')
  const onHandleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setEmail(e.target.value)
  }
  const onHandlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value)
  }
  return (
    <section className={style.main}>
      <div className={style.input_container}>
        <div className={style.outer}>
          <div className={style.inner}>
            <span className={style.inner_label}>이메일</span>
            <input
              placeholder="whatmeow@example.com"
              className={style.inner_input}
              value={email}
              onChange={onHandleEmailChange}
            />
          </div>
        </div>
        <div className={style.outer}>
          <div className={style.inner}>
            <span className={style.inner_label}>비밀번호</span>
            <input
              placeholder="비밀번호 입력"
              className={style.inner_input}
              type="password"
              value={password}
              onChange={onHandlePasswordChange}
            />
          </div>
        </div>
      </div>
      <div className={style.login_btn_container}>
        <button type="button" className={style.login_btn}>
          <span>로그인</span>
        </button>
      </div>
    </section>
  )
}

export default LoginForm
