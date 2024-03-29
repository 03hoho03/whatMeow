import React from 'react'
import style from './page.module.css'
import FeedList from './_components/FeedList'
import { getQueryClient } from '@/app/getQueryClient'
import { dehydrate } from '@tanstack/react-query'
import Hydrate from '@/app/_utils/hydrate.client'
import { BASE_URL, FEED_SIZE } from '@/app/_utils/constants'
import { cookies } from 'next/headers'
import { GetRecentListApiResponse } from '@/app/_services/feedService'

const getCookie = async (key: string) => {
  return cookies().get(key)?.value ?? ''
}

const getAllList = async (
  page = 0,
  limit = 3,
): Promise<GetRecentListApiResponse> => {
  const accessToken = await getCookie('accessToken')
  const param = new URLSearchParams({
    size: limit.toString(),
  })

  if (page > 0) {
    param.append('key', page.toString())
  }

  const response = await fetch(`${BASE_URL}/api/v2/post/search/main?` + param, {
    credentials: 'include',
    cache: 'no-store',
    headers: {
      Cookie: `accessToken=${accessToken}`,
    },
  })

  if (!response.ok) {
    throw new Error('오류가 발생하였습니다.')
  }

  return await response.json()
}

const UserFeed = async () => {
  const queryClient = getQueryClient()

  await queryClient.prefetchInfiniteQuery({
    queryKey: ['hydrate-feeds'],
    queryFn: ({ pageParam }) => getAllList(pageParam, FEED_SIZE),
    initialPageParam: 0,
  })
  const dehydratedState = dehydrate(queryClient)

  return (
    <Hydrate state={dehydratedState}>
      <div className={style.main_wrapper}>{<FeedList />}</div>
    </Hydrate>
  )
}

export default UserFeed
