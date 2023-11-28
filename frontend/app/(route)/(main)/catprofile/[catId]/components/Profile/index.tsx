'use client'
import React from 'react'
import style from './profile.module.css'

const Profile = () => {
  return (
    <section className={style.profileContainer}>
      <div className={style.profileImgWrapper}>
        <div className={style.ProfileImg}></div>
      </div>
      <div className={style.catNameWrapper}>
        <span className={style.catName}>네로</span>
      </div>
      <p className={style.catIntroduce}>{'꽤 귀여워요'}</p>
      <button type="button" className={style.EditBtn}>
        프로필 편집
      </button>
    </section>
  )
}

export default Profile
