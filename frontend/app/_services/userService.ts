import { useFetch } from '../_helpers/client/useFetch'
import { BASE_URL } from '../_utils/constants'

export interface GetUserProfileResponse {
  userId: number
  nickname: string
  profileThumnail: string
  postCount: number
  explain: string
  follow: Follow
  cats: Cat[]
  posts: Post[]
  owner: boolean
}
interface Post {
  postId: number
  thumnail: string
}
interface Cat {
  catName: string
  catId: number
  thumnail: string
}
interface Follow {
  followerCount: number
  followingCount: number
  isFollowing: boolean
}
export interface UserCatApiResponse {
  catName: string
  catId: number
}

interface UserService {
  checkDuplicated: (nickname: string) => Promise<void>
  updateUser: (file: FormData) => Promise<void>
  getUserProfile: (nickname: string) => Promise<GetUserProfileResponse>
  getUserCat: () => Promise<UserCatApiResponse[]>
}

function useUserService(): UserService {
  const fetch = useFetch()
  const baseUrl = `${BASE_URL}/api/v2/users`
  return {
    checkDuplicated: async (nickname) => {
      const response = await fetch.get(`${baseUrl}/duplicated`, {
        body: { nickname },
      })

      if (!response.ok) {
        throw new Error('오류가 발생하였습니다.')
      }

      return await response.json()
    },
    updateUser: async (file) => {
      const response = await fetch.put(`${baseUrl}/update`, {
        body: file,
        options: { credentials: 'include' },
      })

      if (!response.ok) {
        throw new Error('오류가 발생하였습니다.')
      }

      return await response.json()
    },
    getUserProfile: async (nickname) => {
      const response = await fetch.get(`${baseUrl}/profile/${nickname}`, {
        options: { credentials: 'include' },
      })

      if (!response.ok) {
        throw new Error('오류가 발생하였습니다.')
      }

      return await response.json()
    },
    getUserCat: async () => {
      const response = await fetch.get(`${baseUrl}/cat`, {
        options: { credentials: 'include' },
      })

      if (!response.ok) {
        throw new Error('오류가 발생하였습니다.')
      }

      return await response.json()
    },
  }
}

export default useUserService
