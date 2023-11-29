import React from 'react'
import style from './page.module.css'
import FeedList from './_components/FeedList'
import { getQueryClient } from '@/app/getQueryClient'
import { dehydrate } from '@tanstack/react-query'
import Hydrate from '@/app/_utils/hydrate.client'
import { BASE_URL, FEED_SIZE } from '@/app/_utils/constants'
import { FeedItem } from '@/app/_services/searchService'
import { cookies } from 'next/headers'

const getCookie = async (key: string) => {
  return cookies().get(key)?.value ?? ''
}

const getAllList = async (page = 0, limit = 3): Promise<FeedItem> => {
  const accessToken = await getCookie('accessToken')
  const param = new URLSearchParams({
    limit: limit.toString(),
    start: page.toString(),
  })
  const response = await fetch(`${BASE_URL}/api/v1/guest/search?` + param, {
    credentials: 'include',
    headers: {
      Cookie: `accessToken=${accessToken}`,
    },
  })
    .then((res) => res.json())
    .then((data) => {
      const result = data.map((feed: FeedItem) => {
        return {
          ...feed,
          createdAt: new Date(feed.createdAt),
        }
      })
      console.log(result)
      return result
    })
  return response
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
