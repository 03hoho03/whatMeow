import React from 'react'
import style from './bookmarkBtn.module.css'
import { CiBookmark } from 'react-icons/ci'

const BookmarkBtn = () => {
  return (
    <button className={style.menuBtn}>
      <CiBookmark className={style.iconBtn} />
    </button>
  )
}

export default BookmarkBtn
