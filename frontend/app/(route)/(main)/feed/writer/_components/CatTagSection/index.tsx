'use client'
import React, { useState } from 'react'
import style from './catTagSection.module.css'
import cn from 'classnames'
import { FaAngleDown, FaAngleUp } from 'react-icons/fa'
import CatTagOption from '../CatTagOption'
import CatTag from '../CatTag'
import { useRecoilValue } from 'recoil'
import { catTagList } from '@/app/_store/atom/writer/catTag'
import { useUserCatListQuery } from '@/app/_services/quries/useUserCatList'

const CatTagSection = () => {
  const [isToggle, setIsToggle] = useState<boolean>(false)
  const catTag = useRecoilValue(catTagList)
  const { data, isSuccess } = useUserCatListQuery()

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
                  data?.map((catInfo, idx) => {
                    return (
                      <CatTagOption
                        key={`${catInfo.catName}_${idx}`}
                        catInfo={catInfo}
                      />
                    )
                  })}
              </ul>
            </div>
          </div>
        </div>
      </div>
      <div className={style.selectedOptionContainer}>
        {catTag.map(({ catId, catName }, idx) => (
          <CatTag key={`${catId}_${idx}`} catTag={catName} />
        ))}
      </div>
    </section>
  )
}

export default CatTagSection
