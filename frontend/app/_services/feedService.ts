import { useFetch } from '../_helpers/client/useFetch'
import { BASE_URL } from '../_utils/constants'

export { useFeedService }

interface Like {
  count: number
  isLike: boolean
}
interface Comment {
  comment: string
  nickname: string
  thumnail: string
}
export interface PostDetailApiResponse {
  nickname: string
  writerThumnail: string
  postId: number
  like: Like
  content: string
  createdAt: string
  images: string[]
  hashtags: string[]
  comments: Comment[]
}

interface FeedService {
  upload: (form: FormData) => Promise<void>
  registComment: (comment: string) => Promise<void>
  updateLike: (feedId: number) => Promise<Like>
  getPostDetail: (postId: number) => Promise<PostDetailApiResponse>
}

function useFeedService(): FeedService {
  const fetch = useFetch()
  const baseUrl = `${BASE_URL}/api/v1/post`
  return {
    upload: async (form) => {
      const response = await fetch.post(`${baseUrl}`, form, undefined, {
        credentials: 'include',
      })
      if (!response.ok) {
        const error = new Error('게시글 등록에 실패하였습니다.')
        error.cause = response.status
        throw error
      }
      return await response.json()
    },
    registComment: async (data) => {
      console.log(data)
      setTimeout(() => Promise.resolve(true), 1000)
    },
    updateLike: async (feedId) => {
      const response = await fetch.post(
        `${baseUrl}/like/${feedId}`,
        null,
        undefined,
        {
          credentials: 'include',
        },
      )
      if (!response.ok) {
        throw new Error('오류가 발생하였습니다.')
      }
      return await response.json()
    },
    getPostDetail: async (postId) => {
      const response = await fetch.get(
        `${baseUrl}/${postId}`,
        null,
        undefined,
        { credentials: 'include' },
      )
      if (!response.ok) {
        throw new Error('오류가 발생하였습니다.')
      }
      return await response.json()
    },
  }
}
