'use client'
import React from 'react'
import style from './feedItem.module.css'
import FeedHeader from '../FeedHeader'
import FeedBody from '../FeedBody'
import FeedBottomMenu from '../FeedBottomMenu'
import { useQueryClient } from '@tanstack/react-query'

interface FeedItem {
  createdAt: Date
  content: string
  images: string[]
  like: Like
  nickname: string
  writerThumnail: string
  postId: number
}
interface Like {
  count: number
  isLike: boolean
}

interface FeedProps {
  feed: FeedItem
}

const Feed = ({
  feed: { nickname, images, createdAt, like, postId, writerThumnail },
}: FeedProps) => {
  const queryClient = useQueryClient()
  queryClient.setQueryData(['like', postId], like)

  return (
    <li className={style.main_wrapper}>
      <FeedHeader writerThumnail={writerThumnail} nickname={nickname} />
      <FeedBody images={images} />
      <FeedBottomMenu createdAt={createdAt} postId={postId} />
    </li>
  )
}

export default Feed
