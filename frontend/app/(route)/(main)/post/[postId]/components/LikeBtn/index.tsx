import React from 'react'
import style from './likeBtn.module.css'
import cn from 'classnames'
import { TbHeart } from 'react-icons/tb'
import { useUpdateLikeMutation } from '@/app/_services/mutations/useUpdateLike'

interface LikeBtnProps {
  postId: number
  version: number
}

const LikeBtn = ({ postId, version }: LikeBtnProps) => {
  const { likeMutation } = useUpdateLikeMutation()

  const HandleClickLikeBtn = () => {
    likeMutation.mutate({ postId, version })
  }

  return (
    <button className={style.menuBtn} onClick={HandleClickLikeBtn}>
      <TbHeart
        className={cn(style.btnIcon, style.likeWBtn, {
          [style.likeBtnActive]: likeMutation.data?.like.isLike,
        })}
      />
    </button>
  )
}

export default LikeBtn
