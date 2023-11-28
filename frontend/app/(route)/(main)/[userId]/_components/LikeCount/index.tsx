import React from 'react'
import style from './likeCount.module.css'
import { useQuery } from '@tanstack/react-query'

interface LikeCountProps {
  postId: string
}
interface Like {
  count: number
  isLike: boolean
}

const LikeCount = ({ postId }: LikeCountProps) => {
  const { data } = useQuery<Like>({ queryKey: ['like', postId] })

  return <span className={style.likeCount}>{`좋아요 ${data?.count}개`}</span>
}

export default LikeCount
