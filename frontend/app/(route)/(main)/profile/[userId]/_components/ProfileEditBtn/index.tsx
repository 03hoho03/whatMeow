import React from 'react'
import style from './profileEditBtn.module.css'
import { useRouter } from 'next/navigation'

const ProfileEditBtn = () => {
  const router = useRouter()
  const handleLinkProfile = () => {
    router.push('/account/edit')
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
