'use client'
import { useGetCommentList } from '@/app/_services/quries/useGetCommentList'
import React from 'react'
import Comment from '../Comment'

const CommentList = ({ postId }: { postId: number }) => {
  const { commentQuery } = useGetCommentList(postId)

  return (
    <div>
      {commentQuery.data ? (
        commentQuery.data.map((comment, idx) => (
          <Comment
            key={comment.nickname + idx}
            comment={comment}
            postId={postId}
          />
        ))
      ) : (
        <></>
      )}
    </div>
  )
}

export default CommentList
