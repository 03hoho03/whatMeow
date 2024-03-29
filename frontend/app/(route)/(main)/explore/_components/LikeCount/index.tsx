import React from 'react'
import style from './likeCount.module.css'
import { useQuery } from '@tanstack/react-query'
import { Like } from '@/app/_services/likeService'

interface LikeCountProps {
  postId: number
}

const LikeCount = ({ postId }: LikeCountProps) => {
  const { data } = useQuery<Like>({ queryKey: ['like', postId] })

  return (
    <span className={style.likeCount}>{`좋아요 ${
      data ? data.count : 0
    }개`}</span>
  )
}

export default LikeCount
