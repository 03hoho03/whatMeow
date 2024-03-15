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
  updateFollow: (
    nickname: string | undefined,
  ) => Promise<UpdateFollowApiResponse>
}

function useFollowService(): UseFollowService {
  const fetch = useFetch()
  const baseUrl = `${BASE_URL}/api/v1/follow`

  return {
    updateFollow: async (nickname) => {
      if (!nickname) {
        throw new Error('닉네임이 없습니다.')
      }
      const response = await fetch.post(
        `${baseUrl}/follow/${nickname}`,
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

export default useFollowService
