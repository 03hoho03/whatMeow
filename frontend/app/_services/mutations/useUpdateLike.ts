import { useMutation, useQueryClient } from '@tanstack/react-query'
import { LikeStateQueryKey } from '../quries/useLike'
import useLikeService, { Like, UpdateLikeApiResponse } from '../likeService'
import { useRecentPostListQuery } from '../quries/useRecentPostList'

interface LikeMutationVariables {
  postId: number
  version: number
}

export const useUpdateLikeMutation = () => {
  const queryClient = useQueryClient()
  const likeService = useLikeService()
  const { refetch } = useRecentPostListQuery()
  const likeMutation = useMutation<
    UpdateLikeApiResponse,
    Error,
    LikeMutationVariables,
    { previousLike: Like | undefined }
  >({
    mutationFn: ({ postId, version }) => likeService.update(postId, version),
    onMutate: async ({ postId }) => {
      await queryClient.cancelQueries({ queryKey: [LikeStateQueryKey, postId] })
      const previousLike = queryClient.getQueryData<Like>([
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

        queryClient.setQueryData<Like>([LikeStateQueryKey, postId], nextLike)
      }

      return { previousLike }
    },
    onSuccess: () => {
      refetch()
    },
    onError: (
      error: Error,
      { postId }: LikeMutationVariables,
      context?: { previousLike: Like | undefined },
    ) => {
      if (context?.previousLike) {
        queryClient.setQueryData<Like>(
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
