import { useMutation, useQueryClient } from '@tanstack/react-query'
import useCommentService from '../commentService'
import { UseCommentQueryKey } from '../quries/useGetCommentList'

interface UploadCommentMutationVariables {
  postId: number
  comment: string
}

export const useUploadComment = () => {
  const commentService = useCommentService()
  const queryClient = useQueryClient()
  const uploadCommentMutation = useMutation<
    { success: boolean },
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
