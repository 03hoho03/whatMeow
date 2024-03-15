import { useQuery } from '@tanstack/react-query'
import useCommentService from '../commentService'

interface Comment {
  commentId: number
  comment: string
  createdAt: string
  nickname: string
  thumnail: string
}

export const UseCommentQueryKey = 'post-commentList'
export const useGetCommentList = (postId: number) => {
  const commentService = useCommentService()
  const commentQuery = useQuery<Comment[]>({
    queryKey: [UseCommentQueryKey, postId],
    queryFn: () => commentService.getList(postId),
  })

  return { commentQuery }
}
