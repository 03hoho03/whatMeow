import { useFetch } from '../_helpers/client/useFetch'
import { BASE_URL } from '../_utils/constants'

interface CatService {
  profileUpload: (form: FormData) => Promise<AddCatProfileApiResponse>
  getCatProfile: (catId: number) => Promise<GetCatProfileApiResponse>
}
export interface AddCatProfileApiResponse {
  catName: string
  explain: string | null
  gender: null
  breed: null
  ownerId: number
  id: number
}
interface GetCatProfileApiResponse {
  ownerNickname: string
  name: string
  explain: string
  image: string
  posts: Post[]
}
interface Post {
  post_id: number
  thumnail: string
}

function useCatService(): CatService {
  const fetch = useFetch()
  const baseUrl = `${BASE_URL}/api/v2/cat`
  return {
    profileUpload: async (form) => {
      const response = await fetch.post(`${baseUrl}`, {
        body: form,
        options: { credentials: 'include' },
      })

      if (!response.ok) {
        throw new Error('오류가 발생하였습니다.')
      }

      return await response.json()
    },
    getCatProfile: async (catId) => {
      const response = await fetch.get(`${baseUrl}/${catId}`, {
        options: { credentials: 'include' },
      })

      if (!response.ok) {
        throw new Error('오류가 발생하였습니다.')
      }

      return await response.json()
    },
  }
}

export default useCatService
