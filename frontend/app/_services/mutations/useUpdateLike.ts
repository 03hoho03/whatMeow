import { useMutation, useQueryClient } from '@tanstack/react-query'
import { useFeedService } from '../feedService'
import { LikeStateQueryKey } from '../quries/useLike'

interface LikeState {
  count: number
  isLike: boolean
}
interface LikeMutationVariables {
  postId: number
}

export const useUpdateLikeMutation = () => {
  const queryClient = useQueryClient()
  const feedService = useFeedService()
  const likeMutation = useMutation<
    LikeState,
    Error,
    LikeMutationVariables,
    { previousLike: LikeState | undefined }
  >({
    mutationFn: ({ postId }) => feedService.updateLike(postId),
    onMutate: async ({ postId }) => {
      await queryClient.cancelQueries({ queryKey: [LikeStateQueryKey, postId] })
      const previousLike = queryClient.getQueryData<LikeState>([
        LikeStateQueryKey,
        postId,
      ])

      if (previousLike) {
        const nextLike = {
          count: previousLike.isLike
            ? previousLike.count - 1
            : previousLike.count + 1,
          isLike: !previousLike.isLike,
        }

        queryClient.setQueryData<LikeState>(
          [LikeStateQueryKey, postId],
          nextLike,
        )
      }

      return { previousLike }
    },
    onSuccess: () => {},
    onError: (
      error: Error,
      { postId }: LikeMutationVariables,
      context?: { previousLike: LikeState | undefined },
    ) => {
      if (context?.previousLike) {
        queryClient.setQueryData<LikeState>(
          [LikeStateQueryKey, postId],
          context.previousLike,
        )
      }
      console.log(error)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: [LikeStateQueryKey] })
    },
  })

  return { likeMutation }
}
