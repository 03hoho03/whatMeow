'use client'
import React from 'react'
import style from './hashtagList.module.css'
import Hashtag from '../Hashtag'
import { useRecoilState } from 'recoil'
import { hashtagList } from '@/app/_store/atom/writer/hashtag'

const HashtagList = () => {
  const [tagList, setTagList] = useRecoilState<string[]>(hashtagList)
  return (
    <ul className={style.tagList}>
      {tagList?.map((hashtag, idx) => {
        return (
          <Hashtag
            key={hashtag}
            hashtag={hashtag}
            idx={idx}
            setTagList={setTagList}
          />
        )
      })}
    </ul>
  )
}

export default HashtagList
