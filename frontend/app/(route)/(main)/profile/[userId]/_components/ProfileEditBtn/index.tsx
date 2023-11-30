import React from 'react'
import style from './profileEditBtn.module.css'

const ProfileEditBtn = () => {
  const handleLinkProfile = () => {
    alert('아직 구현되지 않은 기능입니다.')
  }
  return (
    <button
      type="button"
      onClick={handleLinkProfile}
      className={style.profileEditBtn}
    >
      프로필 편집
    </button>
  )
}

export default ProfileEditBtn
