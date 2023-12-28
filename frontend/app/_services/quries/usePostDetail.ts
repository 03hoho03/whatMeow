import { useQuery, useQueryClient } from '@tanstack/react-query'
import {
  PostDetailApiResponse,
  useFeedService,
} from '@/app/_services/feedService'
import { UseCommentQueryKey } from './useComment'

interface Like {
  count: number
  isLike: boolean
}
interface Comment {
  comment: string
  nickname: string
  thumnail: string
}
interface PostDetail {
  nickname: string
  writerThumnail: string
  postId: number
  like: Like
  content: string
  createdAt: Date
  images: string[]
  hashtags: string[]
  comments: Comment[]
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
    initialData: {
      nickname: '',
      writerThumnail: '',
      postId: 0,
      like: {
        count: 0,
        isLike: false,
      },
      content: '',
      createdAt: '',
      images: [],
      hashtags: [],
      comments: [],
    },
    select: (data) => {
      return {
        ...data,
        createdAt: new Date(data.createdAt),
      }
    },
  })

  queryClient.setQueryData([UseCommentQueryKey, postId], data.comments)

  return { isSuccess, data, isFetching }
}
