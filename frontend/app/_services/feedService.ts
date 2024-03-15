import { useFetch } from '../_helpers/client/useFetch'
import { BASE_URL } from '../_utils/constants'
import { CommentListApiResponse } from './commentService'
import { Like } from './likeService'

export { useFeedService }

export interface PostDetailApiResponse {
  nickname: string
  writerThumnail: string
  postId: number
  version: number
  like: Like
  content: string
  createdAt: string
  images: string[]
  hashtags: string[]
  comments: CommentListApiResponse[]
}
export interface GetFeedListApiResponse {
  posts: Feed[]
  nextKey: number
}
export interface Feed extends Post {}
export interface Post {
  createdAt: string
  content: string
  images: string[]
  version: number
  like: Like
  nickname: string
  writerThumnail: string
  postId: number
}
export interface GetRecentListApiResponse {
  posts: Post[]
  nextKey: number
}

interface FeedService {
  upload: (form: FormData) => Promise<void>
  getPostDetail: (postId: number) => Promise<PostDetailApiResponse>
  getFeedList: (
    page?: number,
    limit?: number,
  ) => Promise<GetFeedListApiResponse>
  getRecentList: (
    page?: number,
    limit?: number,
  ) => Promise<GetRecentListApiResponse>
}

function useFeedService(): FeedService {
  const fetch = useFetch()
  const baseUrl = `${BASE_URL}/api/v2/post`
  return {
    upload: async (form) => {
      const uploadBody = form

      const response = await fetch.post(`${baseUrl}`, {
        body: uploadBody,
        options: { credentials: 'include' },
      })

      if (!response.ok) {
        const data = await response.json()
        console.log(data)
        const error = new Error('게시글 등록에 실패하였습니다.')
        error.cause = response.status
        throw error
      }

      return await response.json()
    },
    getPostDetail: async (postId) => {
      const response = await fetch.get(`${baseUrl}/${postId}`, {
        options: { credentials: 'include' },
      })

      if (!response.ok) {
        throw new Error('오류가 발생하였습니다.')
      }

      return await response.json()
    },
    getFeedList: async (page = 0, limit = 3) => {
      const param = new URLSearchParams({
        size: limit.toString(),
      })

      if (page > 0) {
        param.append('key', page.toString())
      }

      const response = await fetch.get(`${baseUrl}/search/follow?` + param, {
        options: { credentials: 'include' },
      })

      if (!response.ok) {
        throw Error('오류가 발생하였습니다.')
      }

      return await response.json()
    },
    getRecentList: async (page = 0, limit = 5) => {
      const param = new URLSearchParams({
        size: limit.toString(),
      })

      if (page > 0) {
        param.append('key', page.toString())
      }

      const response = await fetch.get(`${baseUrl}/search/main?` + param, {
        options: { credentials: 'include' },
      })

      if (!response.ok) {
        throw Error('오류가 발생하였습니다.')
      }

      return await response.json()
    },
  }
}
