'use client'
import React from 'react'
import style from './feedItem.module.css'
import FeedHeader from '../FeedHeader'
import FeedBody from '../FeedBody'
import FeedBottomMenu from '../FeedBottomMenu'
import { useQueryClient } from '@tanstack/react-query'
import { SelectedPost } from '@/app/_services/quries/useRecentPostList'

interface FeedProps {
  feed: SelectedPost
}

const Feed = ({
  feed: { nickname, images, createdAt, like, postId, writerThumnail, version },
}: FeedProps) => {
  const queryClient = useQueryClient()
  queryClient.setQueryData(['like', postId], like)

  return (
    <li className={style.main_wrapper}>
      <FeedHeader writerThumnail={writerThumnail} nickname={nickname} />
      <FeedBody images={images} />
      <FeedBottomMenu createdAt={createdAt} postId={postId} version={version} />
    </li>
  )
}

export default Feed
