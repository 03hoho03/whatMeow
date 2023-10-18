import React from 'react'
import JoinForm from './_components/JoinForm'
import style from './page.module.css'

function JoinPage() {
  return (
    <div className={style.main_wrapper}>
      <JoinForm />
    </div>
  )
}

export default JoinPage
