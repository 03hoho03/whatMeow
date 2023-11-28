import React from 'react'
import style from './page.module.css'
import WriterForm from './components/WriterForm'

const CatAddPage = () => {
  return (
    <div className={style.CatAddPageContainer}>
      <WriterForm />
    </div>
  )
}

export default CatAddPage
