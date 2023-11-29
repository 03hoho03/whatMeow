'use client'
import React from 'react'
import { AiFillHome } from 'react-icons/ai'
import { FaClipboardCheck } from 'react-icons/fa'
import { FaSearch } from 'react-icons/fa'
import { FaBell } from 'react-icons/fa'
import { FaUser } from 'react-icons/fa'
import Link from 'next/link'
import style from './bottomMenu.module.css'
import { userAtom } from '@/app/_store/atom/user'
import { useRecoilValue } from 'recoil'

const BottomMenu = () => {
  const { user, isAuth } = useRecoilValue(userAtom)

  return isAuth ? (
    <section className={style.bottomMenuContainer}>
      <div className={style.util_wrapper}>
        <Link href="/" className={style.link}>
          <AiFillHome className={style.icon} />
          <span>메인</span>
        </Link>
        <Link href={`/feed/${user.nickname}`} className={style.link}>
          <FaClipboardCheck className={style.icon} />
          <span>피드</span>
        </Link>
        <Link href="/search" className={style.link}>
          <FaSearch className={style.icon} />
          <span>검색</span>
        </Link>
        <Link href={`/alarm/${user.nickname}`} className={style.link}>
          <FaBell className={style.icon} />
          <span>알림</span>
        </Link>
        <Link href={`/profile/${user.nickname}`} className={style.link}>
          <FaUser className={style.icon} />
          <span>내 정보</span>
        </Link>
      </div>
    </section>
  ) : (
    <></>
  )
}

export default BottomMenu
