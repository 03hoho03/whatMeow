import React from 'react'
import style from './page.module.css'
import WriterForm from './_components/WriterForm'
import ModalTrigger from './_components/ModalTrigger'

function WriterPage() {
  return (
    <div className={style.main_wrapper}>
      <WriterForm />
      <ModalTrigger />
    </div>
  )
}

export default WriterPage
