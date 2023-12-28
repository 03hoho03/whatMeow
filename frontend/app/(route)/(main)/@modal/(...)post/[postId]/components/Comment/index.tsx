'use client'
import React, { useState } from 'react'
import style from './comment.module.css'
import CommentOptionDialog from '../CommentOptionDialog'

interface CommentProps {
  comment: CommentInfo
  postId: number
}
interface CommentInfo {
  commentId: number
  comment: string
  createdAt: string
  nickname: string
  thumnail: string
}

const Comment = ({ comment, postId }: CommentProps) => {
  const [isHover, setIsHover] = useState<boolean>(false)

  const handleMouseOver = () => {
    setIsHover(true)
  }
  const handleMouseLeave = () => {
    setIsHover(false)
  }

  return (
    <li
      className={style.commentContainer}
      onMouseOver={handleMouseOver}
      onMouseLeave={handleMouseLeave}
    >
      <div className={style.commentWrapper}>
        <div className={style.writerThumnailContainer}>
          <div className={style.writerThumnailWrapper}>
            <img src={comment.thumnail} />
          </div>
        </div>
        <div className={style.commentInfoContainer}>
          <span>{comment.nickname}</span>
          <p>{comment.comment}</p>
        </div>
      </div>
      <CommentOptionDialog
        commentId={comment.commentId}
        postId={postId}
        isHover={isHover}
      />
    </li>
  )
}

export default Comment
