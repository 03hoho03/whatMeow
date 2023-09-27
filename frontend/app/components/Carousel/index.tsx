'use client'

import React, { useEffect, useRef, useState } from 'react'
import useInterval from '@/app/hooks/useInterval'
import style from './carousel.module.css'

interface CarouselProps {
  carouselList: string[]
  autoPlay: boolean
}

function Carousel({ carouselList, autoPlay }: CarouselProps) {
  const [currIndex, setCurrIndex] = useState<number>(0)
  const [currList, setCurrList] = useState<string[]>([])
  const [isAnimating, setIsAnimating] = useState<boolean>(false)

  const carouselRef = useRef<HTMLUListElement | null>(null)
  useEffect(() => {
    if (carouselList.length !== 0) {
      setCurrList(carouselList)
    }
  }, [carouselList])

  useEffect(() => {
    if (carouselRef.current !== null) {
      carouselRef.current.style.transform = `translateX(-${currIndex}00%)`
    }
  }, [currIndex])

  const handleSwipe = (direction: number) => {
    const newIndex = currIndex + direction
    if (newIndex < 0 || newIndex >= currList.length) {
      return
    }
    if (isAnimating) {
      return
    }
    setIsAnimating(true)

    setCurrIndex((prev) => prev + direction)
    if (carouselRef.current !== null) {
      carouselRef.current.style.transition = 'all 0.7s ease-in-out'
    }

    setTimeout(() => {
      setIsAnimating(false)
      console.log(autoPlay)
    }, 700)
  }
  useInterval(() => {
    handleSwipe(1)
  }, 1000)

  return (
    <div>
      <div>
        <ul className={style.carouselItem} ref={carouselRef}>
          {currList?.map((image, idx) => {
            const key = `${image}-${idx}`
            return (
              <li key={key} className={style.carouselItem}>
                <img
                  src={image}
                  alt="carousel-img"
                  className={style.carouselImage}
                />
              </li>
            )
          })}
        </ul>
      </div>
    </div>
  )
}

export default Carousel
