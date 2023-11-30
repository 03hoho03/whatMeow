'use client'
import React from 'react'
import style from './profile.module.css'

const Profile = ({
  catName,
  thumnail,
  explain,
}: {
  catName: string
  thumnail: string
  explain: string
}) => {
  return (
    <section className={style.profileContainer}>
      <div className={style.profileImgWrapper}>
        <img src={thumnail} alt="프로필썸네일" className={style.ProfileImg} />
      </div>
      <div className={style.catNameWrapper}>
        <span className={style.catName}>{catName}</span>
      </div>
      <p className={style.catIntroduce}>{explain}</p>
      <button type="button" className={style.EditBtn}>
        프로필 편집
      </button>
    </section>
  )
}

export default Profile
