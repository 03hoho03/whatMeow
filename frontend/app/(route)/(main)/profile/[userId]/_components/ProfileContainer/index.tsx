'use client'
import React, { useEffect } from 'react'
import style from './profileContainer.module.css'
import UserInfo from '../UserInfo'
import MyCatProfiles from '../CatProfiles'
import PostList from '../PostList'
import useUserService from '@/app/_services/userService'
import { useQuery, useQueryClient } from '@tanstack/react-query'

const ProfileContainer = ({ nickname }: { nickname: string }) => {
  const queryClient = useQueryClient()
  const userService = useUserService()
  const profileQuery = useQuery({
    queryKey: ['hydrate-profile'],
    queryFn: () => userService.getUserProfile(nickname),
  })

  useEffect(() => {
    queryClient.setQueryData(['follow', nickname], {
      follow: profileQuery.data?.follow,
    })
  }, [profileQuery.isSuccess])

  return profileQuery.isFetching ? (
    <p>로딩중...</p>
  ) : (
    <div className={style.profileContainer}>
      <UserInfo nickname={nickname} />
      <MyCatProfiles />
      <PostList />
    </div>
  )
}

export default ProfileContainer
