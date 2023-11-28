import React from 'react'
import style from './page.module.css'
import UploadForm from './_components/UploadForm'
import Result from './_components/Result'
import ModalTrigger from './_components/ModalTrigger'

const BreedAiPage = () => {
  return (
    <div className={style.breedAiPageContainer}>
      <h3>알아보고 싶은 고양이 사진을 넣어보세요</h3>
      <UploadForm />
      <Result />
      <ModalTrigger />
    </div>
  )
}

export default BreedAiPage
