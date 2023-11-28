'use client'
import React, { useState } from 'react'
import style from './catTagSection.module.css'
import cn from 'classnames'
import { FaAngleDown, FaAngleUp } from 'react-icons/fa'
import CatTagOption from '../CatTagOption'
import CatTag from '../CatTag'
import { useRecoilValue } from 'recoil'
import { catTagList } from '@/app/_store/atom/writer/catTag'
import { useQuery } from '@tanstack/react-query'
import useUserService from '@/app/_services/userService'

const CatTagSection = () => {
  const [isToggle, setIsToggle] = useState<boolean>(false)
  const catTag = useRecoilValue(catTagList)
  const userService = useUserService()
  const { data, isSuccess } = useQuery({
    queryKey: ['userCat'],
    queryFn: () => userService.getUserCat(),
  })

  const HandleToggle = () => {
    setIsToggle((prev) => !prev)
  }

  return (
    <section>
      <div className={style.TitleContainer}>
        <h3 className={style.formTitle}>함께있는 고양이</h3>
        <div onClick={HandleToggle} className={style.ToggleBtn}>
          {isToggle ? <FaAngleUp /> : <FaAngleDown />}
          <div
            className={style.optionListWrapper}
            onClick={(e) => e.stopPropagation()}
          >
            <div
              className={cn(style.optionListContainer, {
                [style.hidden]: !isToggle,
              })}
            >
              <ul className={style.optionList}>
                {isSuccess &&
                  data?.map(({ cat }, idx) => (
                    <CatTagOption key={`${cat.name}_${idx}`} catInfo={cat} />
                  ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
      <div className={style.selectedOptionContainer}>
        {catTag.map(({ id, name }, idx) => (
          <CatTag key={`${id}_${idx}`} catTag={name} />
        ))}
      </div>
    </section>
  )
}

export default CatTagSection
