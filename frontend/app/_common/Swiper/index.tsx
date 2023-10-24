'use client'

import React, { useState, ReactNode, MouseEventHandler } from 'react'
import style from './swiper.module.css'

function Swiper({
  children,
  swiperContainer,
}: {
  children: ReactNode
  swiperContainer: React.MutableRefObject<HTMLUListElement | null>
}) {
  const [isMouseDown, setIsMouseDown] = useState<boolean>(false)
  const [startX, setStartX] = useState<number>(0)

  const HandleMouseDown: MouseEventHandler<HTMLElement> = (e) => {
    if (!swiperContainer.current) {
      return
    }
    setIsMouseDown(true)
    setStartX(e.pageX + swiperContainer.current.scrollLeft)
  }
  const HandleMouseMove: MouseEventHandler<HTMLElement> = (e) => {
    if (!isMouseDown) return
    if (swiperContainer.current === null) return

    const { scrollWidth, clientWidth, scrollLeft } = swiperContainer.current
    swiperContainer.current.scrollLeft = startX - e.pageX

    if (scrollLeft === 0) {
      setStartX(e.pageX) // 가장 왼쪽일 때, 움직이고 있는 마우스의 x좌표가 곧 startX로 설정.
    } else if (scrollWidth <= clientWidth + scrollLeft) {
      setStartX(e.pageX + scrollLeft) // 가장 오른쪽일 때, 움직이고 있는 마우스의 x좌표에 현재 스크롤된 길이 scrollLeft의 합으로 설정
    }
  }
  const HandleMouseUp = () => {
    setIsMouseDown(false)
  }
  return (
    <section
      role="presentation"
      className={style.swiper_container}
      onMouseDown={HandleMouseDown}
      onMouseMove={HandleMouseMove}
      onMouseUp={HandleMouseUp}
    >
      {children}
    </section>
  )
}

export default Swiper
