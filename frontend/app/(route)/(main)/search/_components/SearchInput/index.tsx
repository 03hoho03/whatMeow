'use client'
import React from 'react'
import style from './searchInput.module.css'

const SearchInput = () => {
  return (
    <div className={style.main_wrapper}>
      <form className={style.search_form}>
        <input
          className={style.search_input}
          placeholder="검색어를 입력해주세요"
        />
      </form>
    </div>
  )
}

export default SearchInput
