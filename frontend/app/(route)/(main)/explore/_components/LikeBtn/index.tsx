import React from 'react'
import style from './likeBtn.module.css'
import cn from 'classnames'
import { TbHeart } from 'react-icons/tb'
import { useLikeQuery } from '@/app/_services/quries/useLike'
import { useUpdateInfiniteLikeMutation } from '@/app/_services/mutations/useUpdateInfiniteLike'

interface LikeBtnProps {
  postId: number
  version: number
}

const LikeBtn = ({ postId, version }: LikeBtnProps) => {
  const { likeMutation } = useUpdateInfiniteLikeMutation()
  const { likeQuery } = useLikeQuery(postId)

  const HandleClickLikeBtn = () => {
    likeMutation.mutate({ postId, version })
  }

  return (
    <button className={style.menuBtn} onClick={HandleClickLikeBtn}>
      <TbHeart
        size="1.5rem"
        className={cn(style.btnIcon, style.likeWBtn, {
          [style.likeBtnActive]: likeQuery.data?.isLike,
        })}
      />
    </button>
  )
}

export default LikeBtn
