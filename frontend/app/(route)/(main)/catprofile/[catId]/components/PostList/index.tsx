'use client'
import React from 'react'
import style from './postLists.module.css'
import { RxDashboard } from 'react-icons/rx'
import { useRouter } from 'next/navigation'

interface Post {
  post_id: number
  thumnail: string
}

const PostList = ({ posts }: { posts: Post[] }) => {
  const router = useRouter()
  const handleClick = (path: number) => {
    router.push(`https://www.whatmeow.shop/post/${path}`)
    // router.push(`/post/${path}`)
  }
  return (
    <div className={style.postListsContainer}>
      <div className={style.header}>
        <RxDashboard className={style.icon} />
      </div>
      <div className={style.postList}>
        {posts ? (
          Array.from({
            length: Math.ceil(posts.length / 3),
          }).map((_, rowIdx) => (
            <div key={rowIdx + 1000} className={style.postListRow}>
              {posts.slice(rowIdx * 3, (rowIdx + 1) * 3).map((post, colIdx) => (
                <button
                  key={post.thumnail + colIdx}
                  onClick={() => handleClick(post.post_id)}
                  className={style.postThumnail}
                >
                  <img src={post.thumnail} alt="이미지" />
                </button>
              ))}
            </div>
          ))
        ) : (
          <p>게시물이 없습니다.</p>
        )}
      </div>
    </div>
  )
}

export default PostList
