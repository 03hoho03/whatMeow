'use client'
import React from 'react'
import style from './loginForm.module.css'
import { SubmitHandler, useForm } from 'react-hook-form'
import SubmitBtn from '@/app/_common/SubmitBtn'
import { useRouter } from 'next/navigation'
import { useSetRecoilState } from 'recoil'
import { userAtom } from '@/app/_store/atom/user'
import loginModalState from '@/app/_store/atom/loginModalState'
import { useLoginMutation } from '@/app/_services/mutations/useLogin'

interface LoginFormReturn {
  email: string
  password: string
}

function LoginForm() {
  const router = useRouter()
  const {
    register,
    handleSubmit,
    formState: { isValid, errors },
  } = useForm<LoginFormReturn>({ mode: 'onChange' })
  const { loginMutation } = useLoginMutation()
  const setUser = useSetRecoilState(userAtom)
  const setLoginModalState = useSetRecoilState(loginModalState)

  const fields = {
    email: register('email', {
      required: true,
      pattern: /^\S+@\S+$/i,
      maxLength: {
        value: 24,
        message: '이메일은 최대 24자까지 가능합니다.',
      },
    }),
    password: register('password', {
      required: true,
      minLength: {
        value: 6,
        message: '비밀번호는 최소 6자 이상 설정해주세요.',
      },
      maxLength: {
        value: 24,
        message: '비밀번호는 최대 24자 이하로 설정해주세요.',
      },
    }),
  }
  const onHandleLogin: SubmitHandler<LoginFormReturn> = async ({
    email,
    password,
  }) => {
    loginMutation.mutate(
      { email, password },
      {
        onSuccess: (data) => {
          setUser({ user: data, isAuth: true })
          router.push('/')
        },
        onError: (error) => {
          setLoginModalState(true)
          console.log(error)
        },
      },
    )
  }

  return (
    <form className={style.main_wrapper} onSubmit={handleSubmit(onHandleLogin)}>
      <div className={style.input_container}>
        <div className={style.outer}>
          <div className={style.inner}>
            <span className={style.inner_label}>이메일</span>
            <input
              {...fields.email}
              placeholder="whatmeow@example.com"
              className={style.inner_input}
            />
          </div>
        </div>
        <p className={style.errorMessage}>{errors?.email?.message}</p>
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
        <p className={style.errorMessage}>{errors?.password?.message}</p>
      </div>
      <SubmitBtn isValid={isValid}>
        <span>로그인</span>
      </SubmitBtn>
    </form>
  )
}

export default LoginForm
