import { useFetch } from '../_helpers/client/useFetch'
import { BASE_URL } from '../_utils/constants'

interface FeedItem {
  createdAt: Date
  content: string
  images: string[]
  like: Like
  nickname: string
  postId: number
}
interface Like {
  count: number
  isLike: boolean
}
interface SearchService {
  getAllList: (page?: number, limit?: number) => Promise<FeedItem[]>
}

function useSearchService(): SearchService {
  const fetch = useFetch()
  const baseUrl = `${BASE_URL}/api/v1/search`
  return {
    getAllList: async (page = 0, limit = 3) => {
      const param = new URLSearchParams({
        limit: limit.toString(),
        start: page.toString(),
      })
      const response = await fetch
        .get(`${baseUrl}/test?` + param, null, undefined, {
          credentials: 'include',
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
    },
  }
}

export default useSearchService
