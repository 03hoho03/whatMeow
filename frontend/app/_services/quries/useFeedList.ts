import { useInfiniteQuery } from '@tanstack/react-query'
import { FEED_SIZE } from '@/app/_utils/constants'
import { Like } from '../likeService'
import { Feed, useFeedService } from '../feedService'

export interface SelectedFeed {
  createdAt: Date
  content: string
  images: string[]
  like: Like
  nickname: string
  writerThumnail: string
  postId: number
  version: number
}

const transformFeedArray = (feeds: Feed[]): SelectedFeed[] => {
  const transformFeed = (feed: Feed) => ({
    ...feed,
    createdAt: new Date(feed.createdAt),
  })

  return feeds.map((feed) => transformFeed(feed))
}

export const UseFeedListQueryKey = 'hydrate-feeds'

export const useFeedListQuery = () => {
  const feedService = useFeedService()
  const {
    data,
    error,
    status,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfiniteQuery({
    queryKey: [UseFeedListQueryKey],
    queryFn: ({ pageParam }) => feedService.getFeedList(pageParam, FEED_SIZE),
    initialPageParam: 0,
    getNextPageParam: (lastPage) => {
      if (lastPage.nextKey <= 1) {
        return null
      }
      return lastPage.nextKey
    },
    select: (data) => ({
      pages: data.pages.map((feeds) => transformFeedArray(feeds.posts)),
      pageParams: data.pageParams,
    }),
  })

  return { data, error, status, fetchNextPage, hasNextPage, isFetchingNextPage }
}
