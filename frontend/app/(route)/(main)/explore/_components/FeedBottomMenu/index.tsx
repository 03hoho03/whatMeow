'use client'
import React, { useEffect, useState } from 'react'
import style from './feedBottomMenu.module.css'
import calcDate from '@/app/_utils/calcDate'
import LikeBtn from '../LikeBtn'
import CommentLink from '../CommentLink'
import BookmarkBtn from '../BookmarkBtn'
import LikeCount from '../LikeCount'

interface FeedBottomMenuProps {
  postId: number
  createdAt: Date
}

const FeedBottomMenu = ({ createdAt, postId }: FeedBottomMenuProps) => {
  const [time, setTime] = useState<string>(createdAt.toLocaleDateString())

  useEffect(() => {
    setTime(calcDate(createdAt))
  }, [createdAt])

  return (
    <section className={style.main_wrapper}>
      <div className={style.menu1}>
        <div className={style.menu_btns}>
          <LikeBtn postId={postId} />
          <CommentLink postId={postId} />
        </div>
        <div className={style.menu_right}>
          <span className={style.created_span}>{time}</span>
          <BookmarkBtn />
        </div>
      </div>
      <div>
        <LikeCount postId={postId} />
      </div>
    </section>
  )
}

export default FeedBottomMenu
