import React from 'react'
import style from './likeBtn.module.css'
import cn from 'classnames'
import { AiOutlineHeart, AiFillHeart } from 'react-icons/ai'
import { useUpdateLikeMutation } from '@/app/_services/mutations/useUpdateLike'
import { useLikeQuery } from '@/app/_services/quries/useLike'

interface LikeBtnProps {
  postId: number
}

const LikeBtn = ({ postId }: LikeBtnProps) => {
  const { likeMutation } = useUpdateLikeMutation()
  const { likeQuery } = useLikeQuery(postId)

  const handleClickLikeBtn = () => {
    likeMutation.mutate({ postId })
  }

  return likeQuery.data?.isLike ? (
    <button className={style.menuBtn} onClick={handleClickLikeBtn}>
      <AiFillHeart size="1.5rem" className={style.likeBtn} />
    </button>
  ) : (
    <button className={style.menuBtn} onClick={handleClickLikeBtn}>
      <AiOutlineHeart
        size="1.5rem"
        className={cn(style.unlikeBtn, {
          [style.likeBtnActive]: likeQuery.data?.isLike,
        })}
      />
    </button>
  )
}

export default LikeBtn
