import { useInfiniteQuery } from '@tanstack/react-query'
import { Post, useFeedService } from '../feedService'
import { FEED_SIZE } from '@/app/_utils/constants'
import { Like } from '../likeService'

export interface SelectedPost {
  createdAt: Date
  content: string
  images: string[]
  like: Like
  nickname: string
  writerThumnail: string
  postId: number
  version: number
}
export interface SelectedPostList {
  posts: SelectedPost
  nextKey: number
}

const transformPostArray = (feeds: Post[]): SelectedPost[] => {
  const transformFeed = (feed: Post) => ({
    ...feed,
    createdAt: new Date(feed.createdAt),
  })

  return feeds.map((feed) => transformFeed(feed))
}

export const UseRecentPostListQueryKey = 'hydrate-posts'

export const useRecentPostListQuery = () => {
  const feedService = useFeedService()
  const {
    data,
    error,
    status,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfiniteQuery({
    queryKey: [UseRecentPostListQueryKey],
    queryFn: ({ pageParam }) => feedService.getRecentList(pageParam, FEED_SIZE),
    initialPageParam: 0,
    getNextPageParam: (lastPage) => {
      if (lastPage.nextKey <= 1) {
        return null
      }
      return lastPage.nextKey
    },
    select: (data) => ({
      pages: data.pages.map((posts) => transformPostArray(posts.posts)),
      pageParams: data.pageParams,
    }),
  })

  return { data, error, status, fetchNextPage, hasNextPage, isFetchingNextPage }
}
