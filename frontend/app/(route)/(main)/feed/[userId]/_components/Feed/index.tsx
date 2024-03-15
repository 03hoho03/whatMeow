'use client'
import React, { useEffect } from 'react'
import style from './feedItem.module.css'
import FeedHeader from '../FeedHeader'
import FeedBody from '../FeedBody'
import FeedBottomMenu from '../FeedBottomMenu'
import { useQueryClient } from '@tanstack/react-query'
import { SelectedFeed } from '@/app/_services/quries/useFeedList'

interface FeedProps {
  feed: SelectedFeed
}

const Feed = ({
  feed: { nickname, images, createdAt, like, postId, writerThumnail, version },
}: FeedProps) => {
  const queryClient = useQueryClient()

  useEffect(() => {
    const existingLike = queryClient.getQueryData(['like', postId])
    console.log(existingLike)
    if (!existingLike) {
      queryClient.setQueryData(['like', postId], like)
    }
  }, [like, postId])

  return (
    <li className={style.main_wrapper}>
      <FeedHeader writerThumnail={writerThumnail} nickname={nickname} />
      <FeedBody images={images} />
      <FeedBottomMenu createdAt={createdAt} postId={postId} version={version} />
    </li>
  )
}

export default Feed
