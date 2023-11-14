'use client'

import React, { useState, useRef } from 'react'
import { FcCameraIdentification, FcTodoList } from 'react-icons/fc'
import { SiEventbrite } from 'react-icons/si'
import Link from 'next/link'
import style from './bookMarkList.module.css'

function BookMarkList() {
  const [isMouseDown, setIsMouseDown] = useState<boolean>(false)
  const [startX, setStartX] = useState<number>(0)

  const bookMarkListRef = useRef<HTMLUListElement | null>(null)
  const onHandleMouseDown = (e: MouseEvent<HTMLElement>) => {
    if (!bookMarkListRef.current) {
      return
    }
    setIsMouseDown(true)
    setStartX(e.pageX + bookMarkListRef.current.scrollLeft)
  }
  const onDragMove = (e: MouseEvent<HTMLElement>) => {
    if (!isMouseDown) {
      return
    }
    if (bookMarkListRef.current === null) {
      return
    }
    const { scrollWidth, clientWidth, scrollLeft } = bookMarkListRef.current
    bookMarkListRef.current.scrollLeft = startX - e.pageX

    if (scrollLeft === 0) {
      setStartX(e.pageX) // 가장 왼쪽일 때, 움직이고 있는 마우스의 x좌표가 곧 startX로 설정.
    } else if (scrollWidth <= clientWidth + scrollLeft) {
      setStartX(e.pageX + scrollLeft) // 가장 오른쪽일 때, 움직이고 있는 마우스의 x좌표에 현재 스크롤된 길이 scrollLeft의 합으로 설정
    }
  }
  const onDragEnd = () => {
    setIsMouseDown(false)
  }
  const throttle = (func, ms: number) => {
    let throttled = false
    return (...args: any[]) => {
      if (!throttled) {
        throttled = true
        setTimeout(() => {
          func(...args)
          throttled = false
        }, ms)
      }
    }
  }
  const delay = 5
  const onThrottleDragMove = throttle(onDragMove, delay)
  return (
    <section
      className={style.main}
      onMouseDown={onHandleMouseDown}
      onMouseMove={isMouseDown ? onThrottleDragMove : null}
      onMouseUp={onDragEnd}
      onMouseLeave={onDragEnd}
    >
      <h1 className={style.title}>즐겨찾기</h1>
      <ul className={style.bookMarkList} ref={bookMarkListRef}>
        <li className={style.bookMarkItem}>
          <Link href="/breedAI">
            <FcCameraIdentification />
            <span>품종 AI</span>
          </Link>
        </li>
        <li className={style.bookMarkItem}>
          <Link href="/meowTest">
            <FcTodoList />
            <span>냥BTI</span>
          </Link>
        </li>
        <li className={style.bookMarkItem}>
          <SiEventbrite />
          <span>이벤트</span>
        </li>
        <li className={style.bookMarkItem}>
          <SiEventbrite />
          <span>다른무언가</span>
        </li>
      </ul>
    </section>
  )
}

export default BookMarkList
