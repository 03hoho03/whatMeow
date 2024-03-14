import { useQuery, useQueryClient } from '@tanstack/react-query'
import {
  PostDetailApiResponse,
  useFeedService,
} from '@/app/_services/feedService'
import { UseCommentQueryKey } from './useGetCommentList'
import { Like } from '../likeService'
import { CommentListApiResponse } from '../commentService'
import { LikeStateQueryKey } from './useLike'

export interface PostDetail {
  nickname: string
  writerThumnail: string
  postId: number
  like: Like
  version: number
  content: string
  createdAt: Date
  images: string[]
  hashtags: string[]
  comments: CommentListApiResponse[]
}

export const UsePostDetailKey = 'hydrate-postDetail'
export const usePostDetail = (postId: number) => {
  const feedService = useFeedService()
  const queryClient = useQueryClient()
  const { isSuccess, data, isFetching } = useQuery<
    PostDetailApiResponse,
    Error,
    PostDetail
  >({
    queryKey: [UsePostDetailKey, postId],
    queryFn: () => feedService.getPostDetail(postId),
    initialData: () => {
      const initialData = {
        nickname: '',
        writerThumnail: '',
        postId: 0,
        version: 0,
        like: {
          count: 0,
          isLike: false,
        },
        content: '',
        createdAt: '',
        images: [],
        hashtags: [],
        comments: [],
      }

      queryClient.setQueryData([LikeStateQueryKey, postId], data.like)
      queryClient.setQueryData([UseCommentQueryKey, postId], data.comments)

      return initialData
    },
    select: (data) => {
      return {
        ...data,
        createdAt: new Date(data.createdAt),
      }
    },
    staleTime: Infinity,
  })

  return { isSuccess, data, isFetching }
}
