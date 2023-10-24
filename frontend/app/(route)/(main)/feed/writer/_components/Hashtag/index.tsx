'use client'
import React from 'react'
import style from './hashtag.module.css'
import { MdCancel } from 'react-icons/md'

interface HashtagProps {
  hashtag: string
  idx: number
  setTagList: React.Dispatch<React.SetStateAction<string[]>>
}
const Hashtag = ({ hashtag, idx, setTagList }: HashtagProps) => {
  const HandleDeleteHashtag = (idx: number) => {
    setTagList((prevTagList) => {
      const newTagList = [...prevTagList]
      newTagList.splice(idx, 1)
      return newTagList
    })
  }
  return (
    <li className={style.hashtag_li}>
      <span className={style.hashtag_content}>{hashtag}</span>
      <button
        className={style.delete_btn}
        onClick={() => HandleDeleteHashtag(idx)}
        type="button"
      >
        <MdCancel className={style.delete_img} />
      </button>
    </li>
  )
}

export default Hashtag
