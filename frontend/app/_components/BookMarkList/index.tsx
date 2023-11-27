'use client'

import React from 'react'
import style from './bookMarkList.module.css'
import { Swiper, SwiperSlide } from 'swiper/react'
import 'swiper/css'
import BookMark from '../BookMark'

const bookMarkInfo = [
  { title: '품종 AI', link: '/breeAI', type: 'camera' },
  { title: '냥BTI', link: '/meowTest', type: 'test' },
  { title: '이벤트', link: '/', type: 'event' },
  { title: '다른무언가', link: '/', type: 'another' },
]

function BookMarkList() {
  return (
    <section className={style.bookMark_container}>
      <h1 className={style.title}>즐겨찾기</h1>
      <Swiper
        slidesPerView={3}
        spaceBetween={20}
        breakpoints={{
          580: {
            slidesPerView: 4,
          },
          760: {
            slidesPerView: 5,
          },
          1000: {
            slidesPerView: 'auto',
          },
        }}
      >
        {bookMarkInfo.map((item) => (
          <SwiperSlide key={item.title} className={style.bookMarkItem}>
            <BookMark info={item} />
          </SwiperSlide>
        ))}
      </Swiper>
    </section>
  )
}

export default BookMarkList
