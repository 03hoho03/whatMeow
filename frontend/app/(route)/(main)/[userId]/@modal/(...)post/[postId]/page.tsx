import Modal from '@/app/_common/Modal'
import React from 'react'
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
  post_id: string,
): Promise<PostDetailApiResponse> => {
  const accessToken = await getCookie('accessToken')
  const Url = `${BASE_URL}/api/v1/post/${post_id}`

  const response = await fetch(Url, {
    method: 'GET',
    credentials: 'include',
    next: {
      revalidate: 30,
    },
    headers: {
      Cookie: `accessToken=${accessToken}`,
    },
  })
  if (!response.ok) {
    throw new Error('오류가 발생하였습니다.')
  }
  console.log(response.status)
  return await response.json()
}

const page = async ({ params }: { params: { postId: string } }) => {
  const queryClient = getQueryClient()
  await queryClient.prefetchQuery({
    queryKey: ['hydrate-postDetail', params.postId],
    queryFn: () => getPostDetail(params.postId),
  })
  const dehydratedState = dehydrate(queryClient)

  return (
    <Hydrate state={dehydratedState}>
      <Modal visible={true}>
        <Post postId={params.postId} />
      </Modal>
    </Hydrate>
  )
}

export default page
