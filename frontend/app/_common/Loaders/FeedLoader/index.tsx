import React from 'react'
import style from './feedLoader.module.css'

const FeedLoader = () => {
  return (
    <div className={style.feedLoaderContainer}>
      <header className={style.postWriterHeader}>
        <div className={style.postWriterThumnail}></div>
        <div className={style.postWriterNickname}></div>
      </header>
      <div className={style.postMediaContent}></div>
    </div>
  )
}

export default FeedLoader
