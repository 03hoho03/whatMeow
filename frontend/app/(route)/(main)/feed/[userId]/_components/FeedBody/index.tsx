'use client'
import React from 'react'
import style from './feedBody.module.css'
import { Navigation, Pagination, A11y } from 'swiper/modules'
import { Swiper, SwiperSlide } from 'swiper/react'
import 'swiper/css'
import 'swiper/css/navigation'
import 'swiper/css/pagination'
import 'swiper/css/scrollbar'

interface FeedBodyProps {
  images: string[]
}

const FeedBody = ({ images }: FeedBodyProps) => {
  return (
    <div className={style.main_wrapper}>
      <Swiper
        modules={[Navigation, Pagination, A11y]}
        slidesPerView={1}
        navigation
        pagination={{ clickable: true }}
        className={style.swiper}
      >
        {images?.map((img) => (
          <SwiperSlide key={img}>
            <img src={img} alt="이미지" className={style.img} />
          </SwiperSlide>
        ))}
      </Swiper>
    </div>
  )
}

export default FeedBody
