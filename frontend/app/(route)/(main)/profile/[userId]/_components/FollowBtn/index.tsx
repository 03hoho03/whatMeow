'use client'
import React from 'react'
import style from './followBtn.module.css'
import cn from 'classnames'
import useFollowService, {
  UpdateFollowApiResponse,
} from '@/app/_services/followService'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

const FollowBtn = ({ nickname }: { nickname: string }) => {
  const queryClient = useQueryClient()
  const followService = useFollowService()
  const followQuery = useQuery<UpdateFollowApiResponse>({
    queryKey: ['follow', nickname],
  })
  const followMutation = useMutation<
    UpdateFollowApiResponse,
    Error,
    void,
    { previousFollow: UpdateFollowApiResponse | undefined }
  >({
    mutationFn: () => followService.updateFollow(nickname),
    onMutate: async () => {
      await queryClient.cancelQueries({ queryKey: ['follow'] })
      const previousFollow = queryClient.getQueryData<UpdateFollowApiResponse>([
        'follow',
        nickname,
      ])

      if (previousFollow) {
        const nextFollow = {
          isFollowing: !previousFollow.follow.isFollowing,
          followerCount: previousFollow.follow.isFollowing
            ? previousFollow.follow.followerCount - 1
            : previousFollow.follow.followerCount + 1,
        }
        queryClient.setQueryData<UpdateFollowApiResponse>(
          ['follow', nickname],
          { follow: nextFollow },
        )
      }
      return { previousFollow }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['follow', nickname] })
    },
  })

  const handleFollow = () => {
    followMutation.mutate()
  }

  return (
    <button
      type="button"
      onClick={handleFollow}
      className={cn(style.followBtn, {
        [style.follow]: followQuery.data?.follow.isFollowing,
      })}
    >
      {followQuery.data?.follow.isFollowing ? '팔로우 취소' : '팔로우'}
    </button>
  )
}

export default FollowBtn
