'use client'
import React from 'react'
import style from './catTagOption.module.css'
import cn from 'classnames'
import { useRecoilState } from 'recoil'
import { catTagList } from '@/app/_store/atom/writer/catTag'

interface CatInfo {
  id: number
  name: string
}
const CatTagOption = ({ catInfo }: { catInfo: CatInfo }) => {
  const [catTag, setCatTag] = useRecoilState(catTagList)

  const HandleTagSelect = () => {
    if (catTag.some((cat) => cat.name.includes(catInfo.name))) {
      setCatTag(catTag.filter((item) => item.name !== catInfo.name))
    } else {
      setCatTag((prev) => [...prev, catInfo])
    }
  }

  return (
    <li
      className={cn(style.option, {
        [style.selected]: catTag.some((cat) => cat.name.includes(catInfo.name)),
      })}
      onClick={HandleTagSelect}
    >
      {catInfo.name}
    </li>
  )
}

export default CatTagOption
