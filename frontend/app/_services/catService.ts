import { useFetch } from '../_helpers/client/useFetch'
import { BASE_URL } from '../_utils/constants'

interface CatService {
  profileUpload: (form: FormData) => Promise<ProfileUploadApiResponse>
}
export interface ProfileUploadApiResponse {
  success: boolean
}

function useCatService(): CatService {
  const fetch = useFetch()
  const baseUrl = `${BASE_URL}/api/v1/cat`
  return {
    profileUpload: async (form) => {
      const response = await fetch.post(`${baseUrl}/add`, form, undefined, {
        credentials: 'include',
      })
      if (!response.ok) {
        throw new Error('오류가 발생하였습니다.')
      }
      return await response.json()
    },
  }
}

export default useCatService
