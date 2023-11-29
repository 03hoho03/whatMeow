import React from 'react'
import style from './modalContent.module.css'

const ModalContent = ({ handleShowModal }: { handleShowModal: () => void }) => {
  return (
    <div>
      <div className={style.modalContentContainer}>
        <div className={style.headerTitle}>
          <h5>로그인 실패</h5>
        </div>
        <div className={style.modalContent}>
          <p>아이디 혹은 비밀번호를 확인해 주세요.</p>
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
