'use client'
import React from 'react'
import style from './pageBackLink.module.css'
import { MdOutlineChevronLeft } from 'react-icons/md'
import { useRouter } from 'next/navigation'

const PageBackLink = () => {
  const router = useRouter()

  return (
    <div className={style.backPageLinkContainer}>
      <button
        type="button"
        onClick={() => router.back()}
        className={style.backPageLink}
      >
        <MdOutlineChevronLeft size={24} />
      </button>
    </div>
  )
}

export default PageBackLink
