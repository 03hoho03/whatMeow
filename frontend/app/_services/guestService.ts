import { useFetch } from '../_helpers/client/useFetch'
import { BASE_URL } from '../_utils/constants'

interface FeedItem {
  createdAt: Date
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
interface GuestService {
  getRecentList: (page?: number, limit?: number) => Promise<FeedItem[]>
}

function useGuestService(): GuestService {
  const fetch = useFetch()
  const baseUrl = `${BASE_URL}/api/v1/guest`

  return {
    getRecentList: async (page = 0, limit = 3) => {
      const param = new URLSearchParams({
        limit: limit.toString(),
        start: page.toString(),
      })
      const response = await fetch
        .get(`${baseUrl}/search?` + param, null, undefined, {
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

export default useGuestService
