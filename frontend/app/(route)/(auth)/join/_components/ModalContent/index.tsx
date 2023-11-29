import React from 'react'
import style from './modalContent.module.css'

const ModalContent = ({ handleShowModal }: { handleShowModal: () => void }) => {
  return (
    <div>
      <div className={style.modalContentContainer}>
        <div className={style.headerTitle}>
          <h5>회원가입 실패</h5>
        </div>
        <div className={style.modalContent}>
          <p>이메일 혹은 닉네임을 확인해 주세요.</p>
        </div>
      </div>
      <button
        type="button"
        onClick={handleShowModal}
        className={style.confirmBtn}
      >
        확인
      </button>
    </div>
  )
}

export default ModalContent
