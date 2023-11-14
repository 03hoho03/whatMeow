'use client'
import React, { useState } from 'react'
import style from './hashtagForm.module.css'
import { useRecoilState } from 'recoil'
import { hashtagList } from '@/app/_store/atom/writer/hashtag'
import { writer } from '@/app/_utils/constants'

const inputErrors = {
  tagStringOver: '한 태그 당 최대 16자 까지 입력해주세요.',
  findSpecial: '특수문자 혹은 공백이 포함되어 있습니다.',
  tagNumOver: '태그는 최대 10개까지 등록 합니다.',
}

const HashtagForm = () => {
  const [tagList, setTagList] = useRecoilState<string[]>(hashtagList)
  const [hashtag, setHashtag] = useState<string>('')
  const [error, setError] = useState<string>('')

  const detectEnter = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault()
      HandleRegistHashtag()
    }
  }
  const HandleChangeInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    setHashtag(e.target.value)
  }
  const HandleRegistHashtag = () => {
    if (tagList.length >= 10) {
      setError(inputErrors.tagNumOver)
      setHashtag('')
      return
    }
    if (hashtag.length > writer.MAX_HASHTAG_LETTER) {
      setError(inputErrors.tagStringOver)
      return
    }

    let newHashtag = hashtag.trim()

    // 중간 공백 제거
    newHashtag = newHashtag.replace(/\s+/g, '')

    const hashtagRegex = /^[a-zA-Z0-9가-힣]+$/
    if (hashtagRegex.test(newHashtag)) {
      setError('')
      setTagList((prev: string[]) => [...new Set([...prev, newHashtag])])
      setHashtag('')
    } else {
      setError(inputErrors.findSpecial)
    }
  }
  return (
    <div className={style.hashtag_input_container}>
      <input
        onChange={HandleChangeInput}
        onKeyDown={detectEnter}
        placeholder="태그를 입력하세요. 최대 16자"
        value={hashtag}
        className={style.hashtag_input}
      />
      <p className={style.hashtag_input_error}>{error}</p>
    </div>
  )
}

export default HashtagForm
