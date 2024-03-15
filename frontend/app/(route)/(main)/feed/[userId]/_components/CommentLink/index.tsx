import React from 'react'
import style from './commentLink.module.css'
import { AiOutlineComment } from 'react-icons/ai'
import Link from 'next/link'

interface CommentLinkProps {
  postId: number
}

const CommentLink = ({ postId }: CommentLinkProps) => {
  return (
    <Link className={style.menuBtn} href={`/post/${postId}`}>
      <AiOutlineComment size="1.5rem" className={style.iconBtn} />
    </Link>
  )
}

export default CommentLink
