'use client'
import React from 'react'
import style from './postMedia.module.css'
import { Pagination, Navigation } from 'swiper/modules'
import { Swiper, SwiperSlide } from 'swiper/react'
import 'swiper/css'
import 'swiper/css/navigation'
import 'swiper/css/pagination'

const PostMedia = ({ images }: { images: string[] }) => {
  return (
    <div className={style.swiperContainer}>
      <Swiper
        modules={[Pagination, Navigation]}
        slidesPerView={1}
        navigation
        pagination={{ clickable: true }}
        className={style.swiper}
      >
        {images?.map((img: string) => (
          <SwiperSlide key={img} className={style.slideItem}>
            <img className={style.slideImg} src={img} alt="이미지" />
          </SwiperSlide>
        ))}
      </Swiper>
    </div>
  )
}

export default PostMedia
