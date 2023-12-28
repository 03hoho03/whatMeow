'use client'
import React from 'react'
import style from './post.module.css'
import PostMedia from '../PostMedia'
import LikeBtn from '../LikeBtn'
import BookmarkBtn from '../BookmarkBtn'
import LikeCount from '../LikeCount'
import CommentForm from '../CommentForm'
import WriterInfoHeader from '../WriterInfoHeader'
import PostContent from '../PostContent'
import { usePostDetail } from '@/app/_services/quries/usePostDetail'
import PostCreatedAt from '../PostCreatedAt'

interface PostProps {
  postId: number
}

const Post = ({ postId }: PostProps) => {
  const { isSuccess, data, isFetching } = usePostDetail(postId)

  if (isFetching) return <p>...로딩중</p>
  if (isSuccess) {
    return (
      <div className={style.postWrapper}>
        <WriterInfoHeader
          writerThumnail={data?.writerThumnail}
          nickname={data?.nickname}
        />
        <PostMedia images={data?.images} />
        <div className={style.noneMediaContainer}>
          <header className={style.userInfoContainer}>
            <div className={style.writerThumnailWrapper}>
              <img src={data.writerThumnail} />
            </div>
            <div>{data.nickname}</div>
          </header>
          <PostContent
            postId={postId}
            content={data?.content}
            hashtags={data?.hashtags}
          />
          <div className={style.userInteractContainer}>
            <div className={style.userInteractBtnsContainer}>
              <LikeBtn postId={data?.postId} />
              <BookmarkBtn />
            </div>
            <div className={style.likeCountContainer}>
              <LikeCount postId={data?.postId} />
            </div>
            <div className={style.createdAtContainer}>
              <PostCreatedAt createdAt={data?.createdAt} />
            </div>
            <CommentForm postId={data?.postId} />
          </div>
        </div>
      </div>
    )
  }
}

export default Post
