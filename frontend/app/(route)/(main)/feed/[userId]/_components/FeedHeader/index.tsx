import React from 'react'
import style from './feedHeader.module.css'
import Link from 'next/link'

interface FeedHeaderProps {
  nickname: string
  writerThumnail: string
}
const FeedHeader = ({ nickname, writerThumnail }: FeedHeaderProps) => {
  return (
    <header className={style.headerContainer}>
      <div className={style.headerWrapper}>
        <Link href={`/profile/${nickname}`} className={style.headerProfileLink}>
          <img src={writerThumnail} className={style.writerThumnailImg} />
        </Link>
        <Link href={`/profile/${nickname}`} className={style.headerProfileLink}>
          {nickname}
        </Link>
      </div>
    </header>
  )
}

export default FeedHeader
