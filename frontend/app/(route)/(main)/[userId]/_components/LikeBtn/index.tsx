import React from 'react'
import style from './likeBtn.module.css'
import cn from 'classnames'
import { TbHeart } from 'react-icons/tb'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useFeedService } from '@/app/_services/feedService'

interface LikeBtnProps {
  postId: string
}
interface Like {
  count: number
  isLike: boolean
}
interface MutateLikeVariables {
  postId: string
}

const LikeBtn = ({ postId }: LikeBtnProps) => {
  const feedService = useFeedService()
  const queryClient = useQueryClient()
  const { data } = useQuery<Like>({ queryKey: ['like', postId] })
  const likeMutation = useMutation<
    Like,
    Error,
    MutateLikeVariables,
    { previousLike: Like | undefined }
  >({
    mutationFn: ({ postId }) => feedService.updateLike(postId),
    onMutate: async ({ postId }) => {
      await queryClient.cancelQueries({ queryKey: ['like', postId] })
      const previousLike = queryClient.getQueryData<Like>(['like', postId])

      if (previousLike) {
        const nextLike = {
          count: previousLike.isLike
            ? previousLike.count - 1
            : previousLike.count + 1,
          isLike: !previousLike.isLike,
        }

        queryClient.setQueryData<Like>(['like', postId], nextLike)
      }
      return { previousLike }
    },
    onSuccess: (data) => {
      console.log(data)
    },
    onError: (
      error: Error,
      variables: MutateLikeVariables,
      context?: { previousLike: Like | undefined },
    ) => {
      if (context?.previousLike) {
        queryClient.setQueryData<Like>(['like', postId], context.previousLike)
      }
      console.log(error)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['like'] })
    },
  })

  const HandleClickLikeBtn = () => {
    likeMutation.mutate({ postId })
  }

  return (
    <button className={style.menuBtn} onClick={HandleClickLikeBtn}>
      <TbHeart
        size="1.5rem"
        className={cn(style.btnIcon, style.likeWBtn, {
          [style.likeBtnActive]: data?.isLike,
        })}
      />
    </button>
  )
}

export default LikeBtn
