'use client'
import React, { useRef } from 'react'
import Feed from '../Feed'
import { useInfiniteQuery } from '@tanstack/react-query'
import useSearchService from '@/app/_services/searchService'
import { useObserver } from '@/app/_hooks/useUserObserver'
import { FEED_SIZE } from '@/app/_utils/constants'

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

const FeedList = () => {
  const searchService = useSearchService()
  const bottom = useRef<HTMLDivElement | null>(null)
  const {
    data,
    error,
    status,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfiniteQuery({
    queryKey: ['hydrate-feeds'],
    queryFn: ({ pageParam }) => searchService.getFeedList(pageParam, FEED_SIZE),
    initialPageParam: 0,
    getNextPageParam: (lastPage, allPages) => {
      if (lastPage.length < FEED_SIZE) {
        return null
      }
      return allPages.length // 다음 페이지 번호
    },
  })
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
      {status === 'error' && <p>{error.message}</p>}
      {status === 'success' &&
        data.pages.map((group) =>
          group.map((feed: FeedItem, idx: number) => (
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
