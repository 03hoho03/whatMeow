import React from 'react'
import style from './page.module.css'
import FeedList from './_components/FeedList'
import { getQueryClient } from '@/app/getQueryClient'
import { dehydrate } from '@tanstack/react-query'
import Hydrate from '@/app/_utils/hydrate.client'
import { FEED_SIZE } from '@/app/_utils/constants'
import useSearchService from '@/app/_services/searchService'

const UserFeed = async () => {
  const queryClient = getQueryClient()
  const searchService = useSearchService()
  await queryClient.prefetchInfiniteQuery({
    queryKey: ['hydrate-feeds'],
    queryFn: ({ pageParam }) => searchService.getAllList(pageParam, FEED_SIZE),
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
