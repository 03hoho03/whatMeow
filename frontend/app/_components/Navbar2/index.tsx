'use client'

import React, { useEffect, useState } from 'react'

import cn from 'classnames'
import Link from 'next/link'
import { useRouter, usePathname } from 'next/navigation'
import { useRecoilState } from 'recoil'
import { authState } from '@/app/_store/atom/auth'

import style from './navbar2.module.css'

const navItems = [
  { name: '투데이', path: '/' },
  { name: '피드', path: '/feed' },
  { name: '검색', path: '/search' },
  { name: '알림', path: '/alarm' },
  { name: '프로필', path: '/profile' },
]

function Navbar2() {
  const [scrollY, setScrollY] = useState(0)
  const [auth, setAuth] = useRecoilState(authState)

  const pathname = usePathname()
  const router = useRouter()
  useEffect(() => {
    const handleScroll = () => {
      setScrollY(window.scrollY)
    }
    window.addEventListener('scroll', handleScroll)

    return () => {
      window.removeEventListener('scroll', handleScroll)
    }
  }, [])
  const onHandleLogout = async () => {
    try {
      await fetch('api/account/logout')
      setAuth(false)
      router.push('/')
    } catch (error) {
      console.error(error)
    }
  }
  return (
    <section
      className={cn(style.main_wrapper, { [style.scrolled]: scrollY > 0 })}
    >
      <h3 className={style.logo_wrapper}>
        <Link href="/">LOGO</Link>
      </h3>
      <nav className={style.nav}>
        <ul className={style.nav_ul}>
          {navItems.map(({ name, path }, idx) => (
            <li key={`${name}-${idx}`}>
              <Link
                href={path}
                className={cn(style.nav_link, {
                  [style.nav_clicked]: pathname === path,
                })}
              >
                {name}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
      <ul className={style.util_ul}>
        {auth ? (
          <li>
            <button
              className={cn(style.util_button, {
                [style.util_scrolled]: scrollY > 0,
              })}
              onClick={onHandleLogout}
              type="button"
            >
              로그아웃
            </button>
          </li>
        ) : (
          <li>
            <Link href="/login">
              <button
                className={cn(style.util_button, {
                  [style.util_scrolled]: scrollY > 0,
                })}
                type="button"
              >
                로그인
              </button>
            </Link>
          </li>
        )}
      </ul>
    </section>
  )
}

export default Navbar2
