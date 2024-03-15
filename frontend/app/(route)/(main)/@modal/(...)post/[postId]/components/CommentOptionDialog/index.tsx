'use client'
import React from 'react'
import style from './commentOptionDialog.module.css'
import cn from 'classnames'
import * as Dialog from '@radix-ui/react-dialog'
import { SlOptionsVertical } from 'react-icons/sl'
import { useDeleteComment } from '@/app/_services/mutations/useDeleteComment'

interface CommentOptionDialogProps {
  commentId: number
  postId: number
  isHover: boolean
}

const CommentOptionDialog = ({
  commentId,
  postId,
  isHover,
}: CommentOptionDialogProps) => {
  const { deleteCommentMutation } = useDeleteComment(postId)
  const handleDeleteComment = () => {
    deleteCommentMutation.mutate({ commentId })
  }

  return (
    <Dialog.Root>
      <div className={style.dialogTriggerWrapper}>
        <Dialog.Trigger
          className={cn(style.dialogTrigger, { [style.visible]: isHover })}
        >
          <button className={style.commentOptionBtn}>
            <SlOptionsVertical className={style.icon} />
          </button>
        </Dialog.Trigger>
      </div>
      <Dialog.Portal>
        <Dialog.Overlay className={style.dialogOverlay} />
        <Dialog.Content className={style.dialogContent}>
          <Dialog.Close asChild>
            <button
              className={style.commentDeleteBtn}
              aria-label="Close"
              type="button"
              onClick={handleDeleteComment}
            >
              삭제
            </button>
          </Dialog.Close>
          <button>수정</button>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  )
}

export default CommentOptionDialog
