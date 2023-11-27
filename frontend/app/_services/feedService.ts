import { useFetch } from '../_helpers/client/useFetch'
import { BASE_URL } from '../_utils/constants'

export { useFeedService }

interface Like {
  count: number
  isLike: boolean
}
interface CommentItem {
  comment: string
}

interface FeedService {
  upload: (form: FormData) => Promise<void>
  registComment: (comment: CommentItem) => Promise<void>
  updateLike: (feedId: number) => Promise<Like>
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
        throw new Error('게시글 등록에 실패하였습니다.')
      }
      return await response.json()
    },
    registComment: async (data: CommentItem) => {
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
  }
}
