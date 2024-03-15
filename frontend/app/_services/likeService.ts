import { useFetch } from '../_helpers/client/useFetch'
import { BASE_URL } from '../_utils/constants'

export interface Like {
  count: number
  isLike: boolean
}
export interface UpdateLikeApiResponse {
  like: Like
  version: number
}
interface LikeService {
  update: (postId: number, version: number) => Promise<UpdateLikeApiResponse>
}

const useLikeService = (): LikeService => {
  const fetch = useFetch()
  const baseUrl = `${BASE_URL}/api/v2/like`
  return {
    update: async (postId, version) => {
      const updateBody = {
        version,
      }

      const response = await fetch.post(`${baseUrl}/${postId}`, {
        headers: {
          'Content-type': 'application/json',
        },
        options: { credentials: 'include' },
        body: updateBody,
      })

      if (!response.ok) {
        throw new Error('오류가 발생하였습니다.')
      }

      return await response.json()
    },
  }
}

export default useLikeService
