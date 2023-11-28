'use client'
import React, { ChangeEvent, FormEvent, useState } from 'react'
import style from './feedCommentInput.module.css'
import { useMutation } from '@tanstack/react-query'
import { useFeedService } from '@/app/_services/feedService'

interface Comment {
  comment: string
}

const FeedCommentInput = () => {
  const [commentInput, setCommentInput] = useState<string>('')
  const feedService = useFeedService()
  const { mutate } = useMutation({
    mutationFn: (variables: Comment) => feedService.registComment(variables),
  })
  const HandleCommentInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    console.log(e.target.value)
    setCommentInput(e.target.value)
  }
  const HandleRegistComment = (e: FormEvent<HTMLFormElement>) => {
    mutate(
      { comment: commentInput },
      {
        onSuccess: () => {
          setCommentInput('')
        },
      },
    )
    e.preventDefault()
    console.log(commentInput)
  }
  return (
    <section className={style.main_wrapper}>
      <div className={style.profile_img}></div>
      <form className={style.commentForm} onSubmit={HandleRegistComment}>
        <input
          placeholder="댓글 달기"
          className={style.comment_input}
          onChange={HandleCommentInputChange}
          value={commentInput}
        />
        <button className={style.commentSubmitBtn} type="submit">
          댓글달기
        </button>
      </form>
    </section>
  )
}

export default FeedCommentInput
