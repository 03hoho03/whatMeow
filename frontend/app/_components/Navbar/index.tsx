'use client'

import React, { useEffect, useState } from 'react'
import cn from 'classnames'
import Link from 'next/link'
import { useRouter, usePathname } from 'next/navigation'
import { useRecoilValue } from 'recoil'
import style from './navbar.module.css'
import { userAtom } from '@/app/_store/atom/user'
import { useAuthService } from '@/app/_services/authService'

const navItems = [
  { name: '투데이', path: '/' },
  { name: '피드', path: '/feed' },
  { name: '검색', path: '/search' },
  { name: '알림', path: '/alarm' },
  { name: '프로필', path: '/profile' },
]

function Navbar() {
  const [scrollY, setScrollY] = useState(0)
  const authService = useAuthService()
  const { user, isAuth } = useRecoilValue(userAtom)

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
  const HandleLogout = async () => {
    authService.logout()
    router.push('/')
  }
  const HandleLogin = () => {
    router.push('/login')
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
          {isAuth &&
            navItems.map(({ name, path }, idx) => (
              <li key={`${name}-${idx}`}>
                <Link
                  href={
                    path === '/' || path === '/search'
                      ? path
                      : path === '/feed'
                      ? user.nickname
                      : `${path}/${user.nickname}`
                  }
                  className={cn(style.nav_link, {
                    [style.nav_clicked]:
                      pathname === path || pathname.startsWith(path + '/'),
                  })}
                >
                  {name}
                </Link>
              </li>
            ))}
        </ul>
      </nav>
      <ul className={style.util_ul}>
        <li>
          <button
            className={cn(style.util_button, {
              [style.util_scrolled]: scrollY > 0,
              [style.hidden]: !isAuth,
            })}
            onClick={HandleLogout}
            type="button"
            disabled={!isAuth}
          >
            로그아웃
          </button>
        </li>
        <li>
          <button
            className={cn(style.util_button, {
              [style.util_scrolled]: scrollY > 0,
              [style.hidden]: isAuth,
            })}
            type="button"
            onClick={HandleLogin}
            disabled={isAuth}
          >
            로그인
          </button>
        </li>
      </ul>
    </section>
  )
}

export default Navbar
