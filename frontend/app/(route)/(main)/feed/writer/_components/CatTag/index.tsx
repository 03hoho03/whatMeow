import React from 'react'
import style from './catTag.module.css'
import { MdCancel } from 'react-icons/md'
import { useSetRecoilState } from 'recoil'
import { catTagList } from '@/app/_store/atom/writer/catTag'

interface CatTagProps {
  catTag: string
}
const CatTag = ({ catTag }: CatTagProps) => {
  const setCatTag = useSetRecoilState(catTagList)
  const HandleDeleteHashtag = () => {
    setCatTag((prevTagList) =>
      prevTagList.filter((item) => item.name !== catTag),
    )
  }

  return (
    <li className={style.hashtag_li}>
      <span className={style.hashtag_content}>{catTag}</span>
      <button
        className={style.delete_btn}
        onClick={() => HandleDeleteHashtag()}
        type="button"
      >
        <MdCancel className={style.delete_img} />
      </button>
    </li>
  )
}

export default CatTag
