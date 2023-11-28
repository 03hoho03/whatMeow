'use client'
import React from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import {
  faHouse,
  faClipboard,
  faMagnifyingGlass,
} from '@fortawesome/free-solid-svg-icons'
import { faBell, faUser } from '@fortawesome/free-regular-svg-icons'
import Link from 'next/link'
import style from './bottomMenu.module.css'
import { userAtom } from '@/app/_store/atom/user'
import { useRecoilValue } from 'recoil'

const BottomMenu = () => {
  const { user, isAuth } = useRecoilValue(userAtom)

  return isAuth ? (
    <div className={style.main_wrapper}>
      <div className={style.util_wrapper}>
        <Link href="/" className={style.link}>
          <button type="button" className={style.button}>
            <FontAwesomeIcon icon={faHouse} className={style.icon} />
            <span>메인</span>
          </button>
        </Link>
        <Link href={`/${user.nickname}`} className={style.link}>
          <button type="button" className={style.button}>
            <FontAwesomeIcon icon={faClipboard} className={style.icon} />
            <span>피드</span>
          </button>
        </Link>
        <Link href="/search" className={style.link}>
          <button type="button" className={style.button}>
            <FontAwesomeIcon icon={faMagnifyingGlass} className={style.icon} />
            <span>검색</span>
          </button>
        </Link>
        <Link href={`/alarm/${user.nickname}`} className={style.link}>
          <button type="button" className={style.button}>
            <FontAwesomeIcon icon={faBell} className={style.icon} />
            <span>알림</span>
          </button>
        </Link>
        <Link href={`/profile/${user.nickname}`} className={style.link}>
          <button type="button" className={style.button}>
            <FontAwesomeIcon icon={faUser} className={style.icon} />
            <span>내 정보</span>
          </button>
        </Link>
      </div>
    </div>
  ) : (
    <></>
  )
}

export default BottomMenu
