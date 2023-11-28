'use client'
import React from 'react'
import style from './postLists.module.css'
import { RxDashboard } from 'react-icons/rx'

const PostList = () => {
  return (
    <div className={style.postListsContainer}>
      <div className={style.header}>
        <RxDashboard className={style.icon} />
      </div>
      <div className={style.postList}>
        <div className={style.postListRow}>
          {Array.from({ length: 3 }).map((_, idx) => (
            <div key={idx} className={style.postThumnail}></div>
          ))}
        </div>
        <div className={style.postListRow}>
          {Array.from({ length: 3 }).map((_, idx) => (
            <div key={idx} className={style.postThumnail}></div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default PostList
