import React from 'react'
import style from './likeCount.module.css'
import { useLikeQuery } from '@/app/_services/quries/useLike'

interface LikeCountProps {
  postId: number
}

const LikeCount = ({ postId }: LikeCountProps) => {
  const { likeQuery } = useLikeQuery(postId)

  return (
    <span className={style.likeCount}>{`좋아요 ${
      likeQuery.data?.count ? likeQuery.data?.count : 0
    }개`}</span>
  )
}

export default LikeCount
