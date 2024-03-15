'use client'
import React from 'react'
import style from './catTagOption.module.css'
import cn from 'classnames'
import { useRecoilState } from 'recoil'
import { catTagList } from '@/app/_store/atom/writer/catTag'
import { UserCatApiResponse } from '@/app/_services/userService'

interface CatTagOptionProps {
  catInfo: UserCatApiResponse
}
const CatTagOption = ({ catInfo }: CatTagOptionProps) => {
  const [catTag, setCatTag] = useRecoilState(catTagList)

  const HandleTagSelect = () => {
    if (catTag.some((cat) => cat.catName.includes(catInfo.catName))) {
      setCatTag(catTag.filter((item) => item.catName !== catInfo.catName))
    } else {
      setCatTag((prev) => [...prev, catInfo])
    }
  }

  return (
    <li
      className={cn(style.option, {
        [style.selected]: catTag.some((cat) =>
          cat.catName.includes(catInfo.catName),
        ),
      })}
      onClick={HandleTagSelect}
    >
      {catInfo.catName}
    </li>
  )
}

export default CatTagOption
