'use client'

import React, { ReactNode } from 'react'
import cn from 'classnames'
import style from './submitBtn.module.css'

interface SubmitBtnProps {
  children: ReactNode
  isValid: boolean
}
const SubmitBtn = ({ children, isValid }: SubmitBtnProps) => {
  return (
    <button
      type="submit"
      className={cn(style.login_btn, { [style.login_enabled]: isValid })}
      disabled={!isValid}
    >
      {children}
    </button>
  )
}

export default SubmitBtn
