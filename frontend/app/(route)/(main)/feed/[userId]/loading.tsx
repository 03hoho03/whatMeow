import React from 'react'
import style from './page.module.css'
import FeedLoader from '@/app/_common/Loaders/FeedLoader'

const Loading = () => {
  return (
    <div className={style.main_wrapper}>
      <FeedLoader />
    </div>
  )
}

export default Loading
