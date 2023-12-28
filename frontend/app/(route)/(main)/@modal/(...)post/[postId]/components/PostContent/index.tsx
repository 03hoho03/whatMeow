import React from 'react'
import style from './postContent.module.css'
import Link from 'next/link'
import CommentList from '../CommentList'

interface PostContentProps {
  postId: number
  content: string
  hashtags: string[]
}

const PostContent = ({ postId, content, hashtags }: PostContentProps) => {
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
      <CommentList postId={postId} />
    </div>
  )
}

export default PostContent
