import {
  InfiniteData,
  useMutation,
  useQueryClient,
} from '@tanstack/react-query'
import { LikeStateQueryKey } from '../quries/useLike'
import useLikeService, { Like, UpdateLikeApiResponse } from '../likeService'
import {
  SelectedPost,
  SelectedPostList,
  UseRecentPostListQueryKey,
} from '../quries/useRecentPostList'

interface LikeMutationVariables {
  postId: number
  version: number
}

export const useUpdateInfiniteLikeMutation = () => {
  const queryClient = useQueryClient()
  const likeService = useLikeService()
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
    onSuccess: (response, { postId }) => {
      queryClient.setQueryData<InfiniteData<Array<SelectedPostList>>>(
        [UseRecentPostListQueryKey],
        (oldData) => {
          console.log(oldData)
          console.log(oldData?.pages.map((page) => page))
          console.log(oldData?.pages.flatMap((page) => page.posts))
          // const newData = oldData?.pages.map((page) =>
          //   page.map((item) => {
          //     console.log('item:', item)
          //     if (item.posts.postId === postId) {
          //       return {
          //         ...item,
          //         like: response.like,
          //         version: response.version,
          //       }
          //     } else {
          //       post
          //     }
          //   }),
          // )
          // return {
          //   ...oldData,
          //   pages: newData,
          // }
        },
      )
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
