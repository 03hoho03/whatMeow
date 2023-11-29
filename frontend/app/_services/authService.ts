import { useFetch } from '../_helpers/client/useFetch'
import { BASE_URL } from '../_utils/constants'

export { useAuthService }

interface AuthSerivce {
  register: (email: string, password: string, username: string) => Promise<void>
  login: (username: string, password: string) => Promise<void>
  logout: () => Promise<void>
}

function useAuthService(): AuthSerivce {
  const fetch = useFetch()
  const baseUrl = `${BASE_URL}/api/v1/auth`
  return {
    register: async (email, password, nickname) => {
      const name = '장호정'
      const response = await fetch.post(
        `${baseUrl}/register`,
        {
          email,
          name,
          password,
          nickname,
        },
        {
          'Content-type': 'application/json',
        },
      )
      if (!response.ok) {
        throw new Error('오류가 발생했습니다.')
      }
      return await response.json()
    },
    login: async (email, password) => {
      const response = await fetch.post(
        `${baseUrl}/login`,
        {
          email,
          password,
        },
        {
          'Content-type': 'application/json',
        },
        { credentials: 'include' },
      )
      if (!response.ok) {
        throw new Error('오류가 발생했습니다.')
      }
      return await response.json()
    },
    logout: async () => {
      const response = await fetch.get(`${baseUrl}/logout`, null, undefined, {
        credentials: 'include',
      })
      if (!response.ok) {
        throw new Error('오류가 발생하였습니다.')
      }
      return await response.json()
    },
  }
}
