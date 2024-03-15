import React from 'react'
import style from './page.module.css'
import { BASE_URL } from '@/app/_utils/constants'
import { cookies } from 'next/headers'
import { GetUserProfileResponse } from '@/app/_services/userService'
import { getQueryClient } from '@/app/getQueryClient'
import { dehydrate } from '@tanstack/react-query'
import Hydrate from '@/app/_utils/hydrate.client'
import ProfileContainer from './_components/ProfileContainer'

const getCookie = async (key: string) => {
  return cookies().get(key)?.value ?? ''
}
const getProfile = async (
  nickname: string,
): Promise<GetUserProfileResponse> => {
  const accessToken = await getCookie('accessToken')
  const response = await fetch(`${BASE_URL}/api/v2/users/profile/${nickname}`, {
    credentials: 'include',
    cache: 'no-store',
    headers: {
      Cookie: `accessToken=${accessToken}`,
    },
  })
  if (!response.ok) {
    throw new Error('에러 발생')
  }
  console.log(response.status)
  return await response.json()
}

const Profile = async ({ params }: { params: { userId: string } }) => {
  const nickname = params.userId
  const queryClient = getQueryClient()
  await queryClient.prefetchQuery({
    queryKey: ['hydrate-profile'],
    queryFn: () => getProfile(nickname),
  })
  const dehydratedState = dehydrate(queryClient)

  return (
    <Hydrate state={dehydratedState}>
      <div className={style.profile_page}>
        <ProfileContainer nickname={nickname} />
      </div>
    </Hydrate>
  )
}

export default Profile
