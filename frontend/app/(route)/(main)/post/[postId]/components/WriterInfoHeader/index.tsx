import React from 'react'
import style from './writerInfoHeader.module.css'

interface WriterInfoHeaderProps {
  writerThumnail: string
  nickname: string
}

const WriterInfoHeader = ({
  writerThumnail,
  nickname,
}: WriterInfoHeaderProps) => {
  return (
    <header className={style.userInfoContainer}>
      <div className={style.writerThumnailWrapper}>
        <img src={writerThumnail} />
      </div>
      <div>{nickname}</div>
    </header>
  )
}

export default WriterInfoHeader
