import React from 'react'
import style from './page.module.css'
import Post from './components/Post'
import { BASE_URL } from '@/app/_utils/constants'
import { cookies } from 'next/headers'
import { getQueryClient } from '@/app/getQueryClient'
import { dehydrate } from '@tanstack/react-query'
import Hydrate from '@/app/_utils/hydrate.client'
import { PostDetailApiResponse } from '@/app/_services/feedService'

const getCookie = async (key: string) => {
  return cookies().get(key)?.value ?? ''
}
const getPostDetail = async (
  post_id: number,
): Promise<PostDetailApiResponse> => {
  const accessToken = await getCookie('accessToken')
  const Url = `${BASE_URL}/api/v2/post/${post_id}`

  const response = await fetch(Url, {
    credentials: 'include',
    cache: 'no-cache',
    headers: {
      Cookie: `accessToken=${accessToken}`,
    },
  })
  if (!response.ok) {
    throw new Error('오류가 발생하였습니다.')
  }
  return await response.json()
}

const page = async ({ params }: { params: { postId: string } }) => {
  const intPostId = parseInt(params.postId)
  const queryClient = getQueryClient()
  await queryClient.prefetchQuery({
    queryKey: ['hydrate-postDetail', intPostId],
    queryFn: () => getPostDetail(intPostId),
  })
  const dehydratedState = dehydrate(queryClient)

  return (
    <Hydrate state={dehydratedState}>
      <div className={style.postDetailPageContainer}>
        <Post postId={intPostId} />
      </div>
    </Hydrate>
  )
}

export default page
