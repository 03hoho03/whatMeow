'use client'
import React from 'react'
import style from './userInfo.module.css'
import FollowBtn from '../FollowBtn'
import ProfileEditBtn from '../ProfileEditBtn'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { GetUserProfileResponse } from '@/app/_services/userService'
import { UpdateFollowApiResponse } from '@/app/_services/followService'

const UserInfo = ({ nickname }: { nickname: string }) => {
  const queryClient = useQueryClient()
  const profileQuery = queryClient.getQueryData<GetUserProfileResponse>([
    'hydrate-profile',
  ])
  const followQuery = useQuery<UpdateFollowApiResponse>({
    queryKey: ['follow', nickname],
  })

  return (
    <div className={style.user_profile_container}>
      <div className={style.user_profile}>
        <div className={style.user_profile_left}>
          <div className={style.userThumnail}>
            <img src={profileQuery?.profileThumnail} alt="유저 썸네일" />
          </div>
        </div>
        <div className={style.user_profile_right}>
          <div className={style.user_profile_detail}>
            <div className={style.user_profile_detail_item}>
              <span className={style.detailCountItem}>
                {profileQuery?.postCount}
              </span>
              <span>게시물</span>
            </div>
            <div className={style.user_profile_detail_item}>
              <span className={style.detailCountItem}>
                {followQuery.data?.follow.followerCount}
              </span>
              <span>팔로워</span>
            </div>
            <div className={style.user_profile_detail_item}>
              <span className={style.detailCountItem}>
                {profileQuery?.follow.followingCount}
              </span>
              <span>팔로잉</span>
            </div>
          </div>
        </div>
      </div>
      <div>
        <span className={style.profileNickname}>{profileQuery?.nickname}</span>
        <p className={style.profileIntroduce}>{profileQuery?.explain}</p>
      </div>
      <div className={style.profileBtnWrapper}>
        {profileQuery?.owner ? (
          <ProfileEditBtn />
        ) : (
          <FollowBtn nickname={nickname} />
        )}
      </div>
    </div>
  )
}

export default UserInfo
