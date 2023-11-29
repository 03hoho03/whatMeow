import { useFetch } from '../_helpers/client/useFetch'
import { BASE_URL } from '../_utils/constants'

export interface BreedAiApiResponse {
  data: BreedAiInfo[]
}
interface BreedAiInfo {
  name: string
  count: number
  feature: string
}
interface UseAiService {
  breedAi: (file: FormData) => Promise<BreedAiApiResponse>
}

function useAiService(): UseAiService {
  const baseUrl = `${BASE_URL}/api/v1/ai`
  const fetch = useFetch()

  return {
    breedAi: async (file) => {
      const response = await fetch.post(`${baseUrl}`, file, undefined, {
        credentials: 'include',
      })
      if (!response.ok) {
        const error = new Error('오류가 발생하였습니다.')
        error.cause = response.status
        throw error
      }
      return await response.json()
    },
  }
}

export default useAiService
