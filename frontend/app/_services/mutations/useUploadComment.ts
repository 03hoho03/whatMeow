import { useMutation, useQueryClient } from '@tanstack/react-query'
import useCommentService, { CommentUploadApiResponse } from '../commentService'
import { UseCommentQueryKey } from '../quries/useGetCommentList'

interface UploadCommentMutationVariables {
  postId: number
  comment: string
}

export const useUploadComment = () => {
  const commentService = useCommentService()
  const queryClient = useQueryClient()
  const uploadCommentMutation = useMutation<
    CommentUploadApiResponse,
    Error,
    UploadCommentMutationVariables
  >({
    mutationFn: ({ postId, comment }) => commentService.upload(comment, postId),
    onSuccess: (_, { postId }) => {
      queryClient.invalidateQueries({ queryKey: [UseCommentQueryKey, postId] })
    },
  })

  return { uploadCommentMutation }
}
