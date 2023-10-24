'use client'

import React from 'react'
import { SubmitHandler, useForm } from 'react-hook-form'
import { useUserService } from '@/app/_services/userService'
import Link from 'next/link'
import style from './joinForm.module.css'
import SubmitBtn from '@/app/_common/SubmitBtn'

interface JoinFormValue {
  email: string
  password: string
  nickname: string
  passwordConfirm: string
}

function JoinForm() {
  const {
    register,
    handleSubmit,
    formState: { isValid, errors },
    getValues,
  } = useForm<JoinFormValue>({ mode: 'onChange' })

  const userService = useUserService()

  const fields = {
    email: register('email', {
      required: '이메일을 입력해주세요.',
      pattern: /^\S+@\S+$/i,
      maxLength: {
        value: 24,
        message: '이메일은 최대 24자까지 가능합니다.',
      },
    }),
    password: register('password', {
      required: '비밀번호를 입력해주세요.',
      minLength: {
        value: 6,
        message: '비밀번호는 최소 6자 이상 설정해주세요.',
      },
      maxLength: {
        value: 24,
        message: '비밀번호는 최대 24자 이하로 설정해주세요.',
      },
    }),
    passwordConfirm: register('passwordConfirm', {
      required: '비밀번호를 확인 해주세요.',
      minLength: 6,
      validate: {
        matchPassword: (value) => {
          const { password } = getValues()
          return password === value || '비밀번호가 일치하지 않습니다.'
        },
      },
    }),
    nickname: register('nickname', {
      required: '닉네임을 입력해주세요.',
      minLength: {
        value: 6,
        message: '최소 6자 이상 입력해주세요.',
      },
      maxLength: 12,
    }),
  }
  const onHandleJoin: SubmitHandler<JoinFormValue> = async (data: any) => {
    const { email, password, nickname } = data
    await userService.join(email, password, nickname)
  }
  const onError = (errors: any) => console.log(errors)
  return (
    <div className={style.main_wrapper}>
      <header>
        <button type="button">
          <Link href="/login">{'<'}</Link>
        </button>
      </header>
      <div className={style.form_explain_wrapper}>
        <h3 className={style.form_explain_title}>이메일 가입</h3>
        <p className={style.form_explain_detail}>
          이메일은 아이디로 사용됩니다.
        </p>
      </div>
      <form
        className={style.input_container}
        onSubmit={handleSubmit(onHandleJoin, onError)}
      >
        <div className={style.outer}>
          <div className={style.inner}>
            <span className={style.inner_label}>이메일</span>
            <input
              {...fields.email}
              placeholder="whatmeow@example.com"
              type="email"
              className={style.inner_input}
            />
          </div>
        </div>
        <div className={style.outer}>
          <div className={style.inner}>
            <span className={style.inner_label}>비밀번호</span>
            <input
              {...fields.password}
              placeholder="비밀번호 입력"
              className={style.inner_input}
              type="password"
            />
          </div>
        </div>
        <div className={style.outer}>
          <div className={style.inner}>
            <span className={style.inner_label}>비밀번호 재입력</span>
            <input
              {...fields.passwordConfirm}
              placeholder="비밀번호 재입력"
              className={style.inner_input}
              type="password"
            />
          </div>
        </div>
        <p className={style.error_message}>
          {errors?.passwordConfirm?.message}
        </p>
        <div className={style.outer}>
          <div className={style.inner}>
            <span className={style.inner_label}>닉네임</span>
            <input
              {...fields.nickname}
              placeholder="닉네임 입력"
              className={style.inner_input}
            />
          </div>
        </div>
        <p className={style.error_message}>{errors?.nickname?.message}</p>
        <SubmitBtn isValid={isValid}>
          <span>회원가입</span>
        </SubmitBtn>
      </form>
    </div>
  )
}

export default JoinForm
