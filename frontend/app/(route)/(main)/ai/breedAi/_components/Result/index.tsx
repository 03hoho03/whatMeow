'use client'
import React from 'react'
import style from './result.module.css'
import { useQuery } from '@tanstack/react-query'

interface BreedAiInfo {
  name: string
  count: number
  feature: string
}

const Result = () => {
  const { data } = useQuery<BreedAiInfo[]>({ queryKey: ['breedAi'] })

  return data ? (
    <div className={style.aiResult}>
      <ul className={style.resultContainer}>
        <span>사진 속에는 </span>
        {data &&
          data.map((cat, idx) => (
            <span
              className={style.catName}
              key={idx}
            >{`${cat.name} 고양이가 ${cat.count}마리`}</span>
          ))}
        <span> 있어요.</span>
      </ul>
      <ul className={style.featureBox}>
        {data &&
          data.map((cat, idx) => (
            <li key={idx}>{`${cat.name}은(는) ${cat.feature}`}</li>
          ))}
      </ul>
    </div>
  ) : (
    <></>
  )
}

export default Result
