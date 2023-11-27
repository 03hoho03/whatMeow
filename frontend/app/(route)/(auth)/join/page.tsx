import React from 'react'
import JoinForm from './_components/JoinForm'
import style from './JoinPage.module.css'
import PageBackLink from './_components/PageBackLink'

function JoinPage() {
  return (
    <div className={style.pageContainer}>
      <PageBackLink />
      <JoinForm />
    </div>
  )
}

export default JoinPage
