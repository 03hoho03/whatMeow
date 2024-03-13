'use client'
import React, { useRef } from 'react'
import Feed from '../Feed'
import { useObserver } from '@/app/_hooks/useUserObserver'
import {
  SelectedPost,
  useRecentPostListQuery,
} from '@/app/_services/quries/useRecentPostList'

const FeedList = () => {
  const bottom = useRef<HTMLDivElement | null>(null)
  const {
    data,
    error,
    status,
    fetchNextPage,
    isFetchingNextPage,
    hasNextPage,
  } = useRecentPostListQuery()

  const onIntersect = (entries: IntersectionObserverEntry[]) => {
    if (status === 'error') {
      console.log(error)
      return
    }
    const firstEntry = entries[0]
    if (hasNextPage && firstEntry.isIntersecting) {
      fetchNextPage()
    }
  }

  useObserver({
    target: bottom,
    onIntersect,
  })

  return (
    <div>
      {status === 'pending' && <p>불러오는 중</p>}
      {status === 'error' && <p>{error?.message}</p>}
      {status === 'success' &&
        data?.pages.map((group) =>
          group.map((feed: SelectedPost, idx: number) => (
            <Feed key={idx} feed={feed} />
          )),
        )}
      <div ref={bottom}></div>
      {isFetchingNextPage && <p>계속 불러오는 중</p>}
      {!hasNextPage && <div>최근 올라온 게시글을 모두 보았습니다.</div>}
    </div>
  )
}

export default FeedList
