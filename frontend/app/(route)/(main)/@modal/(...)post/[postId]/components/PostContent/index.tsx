import React from 'react'
import style from './postContent.module.css'
import Link from 'next/link'
import Comment from '../Comment'

interface PostContentProps {
  content: string
  hashtags: string[]
  comments: CommentInfo[]
}
interface CommentInfo {
  comment: string
  nickname: string
  thumnail: string
}

const PostContent = ({ content, hashtags, comments }: PostContentProps) => {
  return (
    <div className={style.postContentContainer}>
      <p className={style.postContent}>{content}</p>
      <ul className={style.hashtagList}>
        {hashtags.map((hashtag, idx) => (
          <Link
            key={hashtag + idx}
            href={`/search?hashtag=${hashtag}`}
            className={style.hashtag}
          >{`#${hashtag}`}</Link>
        ))}
      </ul>
      <div>
        {comments.map((comment, idx) => (
          <Comment key={comment.nickname + idx} comment={comment} />
        ))}
      </div>
    </div>
  )
}

export default PostContent
