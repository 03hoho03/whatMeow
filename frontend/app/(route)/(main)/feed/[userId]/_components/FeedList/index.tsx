'use client'
import React, { useRef } from 'react'
import Feed from '../Feed'
import { useObserver } from '@/app/_hooks/useUserObserver'
import {
  SelectedFeed,
  useFeedListQuery,
} from '@/app/_services/quries/useFeedList'
import FeedLoader from '@/app/_common/Loaders/FeedLoader'
import { TailSpin } from 'react-loader-spinner'

const FeedList = () => {
  const bottom = useRef<HTMLDivElement | null>(null)
  const {
    data,
    error,
    status,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useFeedListQuery()

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
    <>
      {status === 'pending' && <FeedLoader />}
      {status === 'error' && <p>{error?.message}</p>}
      {status === 'success' &&
        data?.pages.map((group) =>
          group.map((feed: SelectedFeed) => (
            <Feed key={feed.postId} feed={feed} />
          )),
        )}
      <div ref={bottom}></div>
      {isFetchingNextPage && (
        <div style={{ padding: '36px 0' }}>
          <TailSpin height={100} width={100} color="#ff0000" />
        </div>
      )}
      {!hasNextPage && <div>최근 올라온 게시글을 모두 보았습니다.</div>}
    </>
  )
}

export default FeedList
