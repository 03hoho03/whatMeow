'use client'
import React from 'react'
import style from './postLists.module.css'
import { RxDashboard } from 'react-icons/rx'
import Link from 'next/link'
import { GetUserProfileResponse } from '@/app/_services/userService'
import { useQueryClient } from '@tanstack/react-query'

const PostList = () => {
  const queryClient = useQueryClient()
  const profileQuery = queryClient.getQueryData<GetUserProfileResponse>([
    'hydrate-profile',
  ])
  return (
    <div className={style.postListsContainer}>
      <div className={style.header}>
        <RxDashboard className={style.icon} />
      </div>
      <div className={style.postList}>
        {profileQuery?.posts ? (
          Array.from({
            length: Math.ceil(profileQuery?.posts.length / 3),
          }).map((_, rowIdx) => (
            <div key={rowIdx} className={style.postListRow}>
              {profileQuery?.posts
                .slice(rowIdx * 3, (rowIdx + 1) * 3)
                .map((post, colIdx) => (
                  <Link
                    href={`/post/${post.postId}`}
                    key={colIdx}
                    className={style.postThumnail}
                  >
                    <img src={post.thumnail} alt="이미지" />
                  </Link>
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
