import { useFetch } from '../_helpers/client/useFetch'
import { BASE_URL } from '../_utils/constants'

export interface UpdateFollowApiResponse {
  follow: Follow
}
interface Follow {
  isFollowing: boolean
  followerCount: number
}
interface UseFollowService {
  update: (userId: number | undefined) => Promise<UpdateFollowApiResponse>
}

function useFollowService(): UseFollowService {
  const fetch = useFetch()
  const baseUrl = `${BASE_URL}/api/v2/follow`

  return {
    update: async (userId) => {
      if (!userId) {
        throw new Error('닉네임이 없습니다.')
      }

      const response = await fetch.post(`${baseUrl}/${userId}`, {
        options: { credentials: 'include' },
      })

      if (!response.ok) {
        throw new Error('오류가 발생하였습니다.')
      }

      return await response.json()
    },
  }
}

export default useFollowService
