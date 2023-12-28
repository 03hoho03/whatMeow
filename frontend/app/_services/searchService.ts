import { useFetch } from '../_helpers/client/useFetch'
import { BASE_URL } from '../_utils/constants'

export interface GetFeedListApiResponse extends Feed {}
interface GetRecentListApiResponse extends Feed {}
interface Feed {
  createdAt: string
  content: string
  images: string[]
  like: Like
  nickname: string
  writerThumnail: string
  postId: number
}
interface Like {
  count: number
  isLike: boolean
}
interface SearchService {
  getFeedList: (
    page?: number,
    limit?: number,
  ) => Promise<GetFeedListApiResponse[]>
  getRecentList: (
    page?: number,
    limit?: number,
  ) => Promise<GetRecentListApiResponse[]>
}

function useSearchService(): SearchService {
  const fetch = useFetch()
  const baseUrl = `${BASE_URL}/api/v1/search`
  return {
    getFeedList: async (page = 0, limit = 3) => {
      const param = new URLSearchParams({
        limit: limit.toString(),
        start: page.toString(),
      })
      const response = await fetch.get(`${baseUrl}/main?` + param, {
        options: {
          credentials: 'include',
        },
      })

      if (!response.ok) {
        throw Error('오류가 발생하였습니다.')
      }

      return await response.json()
    },
    getRecentList: async (page = 0, limit = 3) => {
      const param = new URLSearchParams({
        limit: limit.toString(),
        start: page.toString(),
      })
      const response = await fetch.get(`${baseUrl}/guest?` + param, {
        options: {
          credentials: 'include',
        },
      })

      if (!response.ok) {
        throw Error('오류가 발생하였습니다.')
      }

      return await response.json()
    },
  }
}

export default useSearchService
