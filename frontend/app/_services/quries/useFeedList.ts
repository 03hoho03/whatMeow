import { useInfiniteQuery } from '@tanstack/react-query'
import useSearchService, { GetFeedListApiResponse } from '../searchService'
import { FEED_SIZE } from '@/app/_utils/constants'

export interface SelectedFeed {
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

const transformFeedArray = (
  feeds: GetFeedListApiResponse[],
): SelectedFeed[] => {
  const transformFeed = (feed: GetFeedListApiResponse) => ({
    createdAt: new Date(feed.createdAt),
    content: feed.content,
    images: feed.images,
    like: feed.like,
    nickname: feed.nickname,
    writerThumnail: feed.writerThumnail,
    postId: feed.postId,
  })

  return feeds.map((feed) => transformFeed(feed))
}

export const UseFeedListQueryKey = 'hydrate-feeds'

export const useFeedListQuery = () => {
  const searchService = useSearchService()
  const {
    data,
    error,
    status,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfiniteQuery({
    queryKey: [UseFeedListQueryKey],
    queryFn: ({ pageParam }) => searchService.getFeedList(pageParam, FEED_SIZE),
    initialPageParam: 0,
    getNextPageParam: (lastPage, allPages) => {
      if (lastPage.length < FEED_SIZE) {
        return null
      }
      return allPages.length // 다음 페이지 번호
    },
    select: (data) => ({
      pages: data.pages.map((feeds) => transformFeedArray(feeds)),
      pageParams: data.pageParams,
    }),
  })

  return { data, error, status, fetchNextPage, hasNextPage, isFetchingNextPage }
}
