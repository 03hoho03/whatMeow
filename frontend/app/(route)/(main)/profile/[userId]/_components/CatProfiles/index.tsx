'use client'
import React from 'react'
import { Swiper, SwiperSlide } from 'swiper/react'
import style from './catProfile.module.css'
import 'swiper/css'
import Link from 'next/link'
import { GetUserProfileResponse } from '@/app/_services/userService'
import { useQueryClient } from '@tanstack/react-query'

const CatProfiles = () => {
  const queryClient = useQueryClient()
  const profileQuery = queryClient.getQueryData<GetUserProfileResponse>([
    'hydrate-profile',
  ])
  return (
    <div className={style.catProfileContainer}>
      <div className={style.header}>
        <h4>마이 냥프로필</h4>
        <Link href={`/cat/add`} className={style.catProfileAddBtn}>
          프로필 추가
        </Link>
      </div>
      {profileQuery?.cats && (
        <Swiper slidesPerView={3}>
          {profileQuery?.cats.map((profile, idx) => (
            <SwiperSlide
              key={`${profile}/${idx}`}
              className={style.profile_item}
            >
              <img
                src={profile.thumnail}
                alt="고양이"
                className={style.profile_image}
              />
              <Link
                href={`/catprofile/${profile.catId}`}
                className={style.profile_name}
              >
                {profile.catName}
              </Link>
            </SwiperSlide>
          ))}
        </Swiper>
      )}
    </div>
  )
}

export default CatProfiles
