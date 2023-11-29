import React from 'react'
import JoinForm from './_components/JoinForm'
import style from './JoinPage.module.css'
import PageBackLink from './_components/PageBackLink'
import ModalTrigger from './_components/ModalTrigger'

function JoinPage() {
  return (
    <div className={style.pageContainer}>
      <PageBackLink />
      <JoinForm />
      <ModalTrigger />
    </div>
  )
}

export default JoinPage
