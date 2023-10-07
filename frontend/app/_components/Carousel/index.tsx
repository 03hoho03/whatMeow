'use client'

import React, { useEffect, useRef, useState } from 'react'
import { FaChevronCircleLeft, FaChevronCircleRight } from 'react-icons/fa'
import useInterval from '@/app/_hooks/useInterval'
import cn from 'classnames'
import style from './carousel.module.css'

interface CarouselList {
  url: string
  text: string
}

interface CarouselProps {
  carouselList: CarouselList[]
}

function Carousel({ carouselList }: CarouselProps) {
  const [currIndex, setCurrIndex] = useState<number>(0)
  const [currList, setCurrList] = useState<CarouselList[]>([...carouselList])
  const [isAnimating, setIsAnimating] = useState<boolean>(false)

  const carouselRef = useRef<HTMLUListElement | null>(null)

  useEffect(() => {
    if (carouselList.length !== 0) {
      const startData = carouselList[0]
      const endData = carouselList[carouselList.length - 1]
      const newList = [endData, ...carouselList, startData]
      setCurrList(newList)
      setCurrIndex(1)
    }
  }, [carouselList])

  useEffect(() => {
    if (carouselRef.current !== null) {
      carouselRef.current.style.transform = `translateX(-${currIndex}00%)`
    }
  }, [currIndex])

  const moveToNthSlide = (index: number) => {
    setTimeout(() => {
      setCurrIndex(index)
      if (carouselRef.current !== null) {
        carouselRef.current.style.transition = ''
      }
    }, 700)
  }
  const offIsAnimation = () => {
    setTimeout(() => {
      setIsAnimating(false)
    }, 700)
  }

  const handleSwipe = (direction: number) => {
    if (isAnimating) {
      return
    }

    setIsAnimating(true)
    const newIndex = currIndex + direction

    if (newIndex === carouselList.length + 1) {
      moveToNthSlide(1)
    }
    if (newIndex === 0) {
      moveToNthSlide(carouselList.length)
    }
    setCurrIndex((prev) => prev + direction)
    if (carouselRef.current !== null) {
      carouselRef.current.style.transition = 'all 0.7s ease-in-out'
    }
    offIsAnimation()
  }

  useInterval(() => {
    handleSwipe(1)
  }, 5000)

  return (
    <div className={style.main}>
      <div className={style.carouselContainer}>
        <FaChevronCircleLeft
          size={20}
          color="#000000"
          opacity={0.5}
          className={cn(style.moveBtn, style.left)}
          onClick={() => handleSwipe(-1)}
        />
        <FaChevronCircleRight
          size={20}
          color="#000000"
          opacity={0.5}
          className={cn(style.moveBtn, style.right)}
          onClick={() => handleSwipe(1)}
        />
        <ul className={style.carouselItems} ref={carouselRef}>
          {currList?.map((image, idx) => {
            const key = `${image.url}-${idx}`
            return (
              <li key={key} className={style.carouselItem}>
                <img
                  src={image.url}
                  alt="carousel-img"
                  className={style.carouselImage}
                />
              </li>
            )
          })}
        </ul>
        <div className={style.carouselTextContainer}>
          <div className={style.monthlyCatBadge}>이달의 고양이</div>
          <div className={style.monthlyCatText}>
            {currList[currIndex]?.text.split('\n').map((line) => (
              <p className={style.carouselText} key={line}>
                {line}
              </p>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Carousel
