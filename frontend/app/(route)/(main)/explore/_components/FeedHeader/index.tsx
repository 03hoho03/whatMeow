import React from 'react'
import style from './feedHeader.module.css'
import Link from 'next/link'

interface FeedHeaderProps {
  nickname: string
}
const FeedHeader = ({ nickname }: FeedHeaderProps) => {
  return (
    <section className={style.header_wrapper}>
      <div className={style.writer_info_wrapper}>
        <Link href={`/profile/${nickname}`} className={style.header_link}>
          <div className={style.writer_info_img}></div>
        </Link>
        <Link href={`/profile/${nickname}`} className={style.header_link}>
          {nickname}
        </Link>
      </div>
    </section>
  )
}

export default FeedHeader
