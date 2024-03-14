import { useQuery } from '@tanstack/react-query'
import useCommentService from '../commentService'

export const UseCommentListKey = 'commentList'
export const useCommentListQuery = (postId: number) => {
  const commentService = useCommentService()
  const { data } = useQuery({
    queryKey: [UseCommentListKey, postId],
    queryFn: () => commentService.getList(postId),
  })

  return { data }
}
