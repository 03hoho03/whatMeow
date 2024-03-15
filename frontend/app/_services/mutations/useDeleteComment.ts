import { useMutation, useQueryClient } from '@tanstack/react-query'
import useCommentService from '../commentService'
import { UseCommentQueryKey } from '../quries/useGetCommentList'

interface DeleteCommentResponse {
  success: boolean
}
interface DeleteCommentMutationVariables {
  commentId: number
}

export const useDeleteComment = (postId: number) => {
  const commentService = useCommentService()
  const queryClient = useQueryClient()
  const deleteCommentMutation = useMutation<
    DeleteCommentResponse,
    Error,
    DeleteCommentMutationVariables
  >({
    mutationFn: ({ commentId }) => commentService.delete(commentId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [UseCommentQueryKey, postId] })
    },
  })

  return { deleteCommentMutation }
}
