'use client'
import React from 'react'
import style from './commentForm.module.css'
import { SubmitHandler, useForm } from 'react-hook-form'
import { useUploadComment } from '@/app/_services/mutations/useUploadComment'

interface CommentFormReturn {
  comment: string
}

const CommentForm = ({ postId }: { postId: number }) => {
  const { register, handleSubmit, reset } = useForm<CommentFormReturn>()
  const { uploadCommentMutation } = useUploadComment()

  const handleUploadComment: SubmitHandler<CommentFormReturn> = ({
    comment,
  }) => {
    uploadCommentMutation.mutate(
      { comment, postId },
      {
        onSuccess: () => {
          reset()
        },
        onError: (error) => {
          console.log(error)
        },
      },
    )
  }

  return (
    <form
      onSubmit={handleSubmit(handleUploadComment)}
      className={style.commentForm}
    >
      <div className={style.commentInputContainer}>
        <input
          {...register('comment', { required: true })}
          placeholder="댓글 달기"
        />
        <button type="submit">게시</button>
      </div>
    </form>
  )
}

export default CommentForm
