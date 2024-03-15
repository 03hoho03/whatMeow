'use client'
import React from 'react'
import style from './commentForm.module.css'
import { SubmitHandler, useForm } from 'react-hook-form'
import useCommentService, {
  CommentUploadApiResponse,
} from '@/app/_services/commentService'
import { useMutation } from '@tanstack/react-query'

interface CommentFormReturn {
  comment: string
}
interface CommentMutationInput {
  postId: number
  comment: string
}

const CommentForm = ({ postId }: { postId: number }) => {
  const { register, handleSubmit, reset } = useForm<CommentFormReturn>()
  const commentService = useCommentService()
  const commentMutation = useMutation<
    CommentUploadApiResponse,
    Error,
    CommentMutationInput
  >({
    mutationFn: ({ comment, postId }) => commentService.upload(comment, postId),
  })

  const handleUploadComment: SubmitHandler<CommentFormReturn> = ({
    comment,
  }) => {
    commentMutation.mutate(
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
