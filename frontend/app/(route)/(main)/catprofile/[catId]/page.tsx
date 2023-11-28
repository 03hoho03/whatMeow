import React from 'react'
import style from './page.module.css'
import Profile from './components/Profile'
import PostList from './components/PostList'

const CatProfile = () => {
  return (
    <div className={style.catProfilePageContainer}>
      <div className={style.catProfileContainer}>
        <Profile />
        <PostList />
      </div>
    </div>
  )
}

export default CatProfile
