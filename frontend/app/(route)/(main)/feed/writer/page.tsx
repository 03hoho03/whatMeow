import React from 'react'
import style from './page.module.css'
import WriterForm from './_components/WriterForm'

function WriterPage() {
  return (
    <div className={style.main_wrapper}>
      <WriterForm />
    </div>
  )
}

export default WriterPage
