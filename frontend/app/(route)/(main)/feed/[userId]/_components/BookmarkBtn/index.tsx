import React from 'react'
import style from './bookmarkBtn.module.css'
import { BsBookmark } from 'react-icons/bs'

const BookmarkBtn = () => {
  return (
    <button className={style.menuBtn}>
      <BsBookmark className={style.iconBtn} />
    </button>
  )
}

export default BookmarkBtn
