import React from 'react'
import HashtagList from '../HashTagList'
import style from './hashtagSection.module.css'
import HashtagForm from '../HashtagForm'

const HashtagSection = () => {
  return (
    <section className={style.main_wrapper}>
      <h3 className={style.form_title}>해시태그</h3>
      <HashtagForm />
      <HashtagList />
    </section>
  )
}

export default HashtagSection
