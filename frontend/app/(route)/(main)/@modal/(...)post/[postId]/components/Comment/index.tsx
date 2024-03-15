'use client'
import React from 'react'
import style from './comment.module.css'

interface CommentProps {
  comment: CommentInfo
}
interface CommentInfo {
  comment: string
  nickname: string
  thumnail: string
}

const Comment = ({ comment }: CommentProps) => {
  return (
    <li className={style.commentContainer}>
      <div className={style.writerThumnailContainer}>
        <div className={style.writerThumnailWrapper}>
          <img src={comment.thumnail} />
        </div>
      </div>
      <div className={style.commentInfoContainer}>
        <span>{comment.nickname}</span>
        <p>{comment.comment}</p>
      </div>
    </li>
  )
}

export default Comment
