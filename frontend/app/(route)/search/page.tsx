import React from 'react'
import style from './page.module.css'
import SearchInput from './_components/SearchInput'
import PostList from './_components/PostList'

function SearchPage() {
  return (
    <div className={style.main_wrapper}>
      <SearchInput />
      <PostList />
    </div>
  )
}

export default SearchPage
