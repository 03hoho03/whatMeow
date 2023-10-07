'use client'

import React, { useEffect, useState } from 'react'
import cn from 'classnames'
import Link from 'next/link'
import style from './navbar2.module.css'

function Navbar2() {
  const [scrollY, setScrollY] = useState(0)

  useEffect(() => {
    const handleScroll = () => {
      // window.scrollY를 사용하여 현재 스크롤 위치를 가져옵니다.
      setScrollY(window.scrollY)
    }

    // 스크롤 이벤트 리스너를 추가합니다.
    window.addEventListener('scroll', handleScroll)

    // 컴포넌트 언마운트 시 이벤트 리스너를 제거합니다.
    return () => {
      window.removeEventListener('scroll', handleScroll)
    }
  }, [])
  return (
    <div className={cn(style.main, { [style.scrolled]: scrollY > 0 })}>
      <div>왓냐옹</div>
      <div>
        <Link href="/login" className={style.navBtn}>
          로그인
        </Link>
      </div>
    </div>
  )
}

export default Navbar2
