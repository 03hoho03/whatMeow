import { useFetch } from '../_helpers/client/useFetch'
import { BASE_URL } from '../_utils/constants'

export { useAuthService }

interface AuthService {
  register: (email: string, password: string, username: string) => Promise<void>
  login: (username: string, password: string) => Promise<void>
  logout: () => Promise<void>
  kakao: () => Promise<void>
}

function useAuthService(): AuthService {
  const fetch = useFetch()
  const baseUrl = `${BASE_URL}/api/v1/auth`
  return {
    register: async (email, password, nickname) => {
      const name = '장호정'
      const response = await fetch.post(`${baseUrl}/register`, {
        headers: {
          'Content-type': 'application/json',
        },
        body: {
          email,
          name,
          password,
          nickname,
        },
      })

      if (!response.ok) {
        throw new Error('오류가 발생했습니다.')
      }

      return await response.json()
    },
    login: async (email, password) => {
      const response = await fetch.post(`${baseUrl}/login`, {
        headers: {
          'Content-type': 'application/json',
        },
        body: {
          email,
          password,
        },
        options: { credentials: 'include' },
      })

      if (!response.ok) {
        throw new Error('오류가 발생했습니다.')
      }

      return await response.json()
    },
    logout: async () => {
      const response = await fetch.get(`${baseUrl}/logout`, {
        options: { credentials: 'include' },
      })

      if (!response.ok) {
        const error = new Error('오류가 발생하였습니다.')
        error.cause = response.status

        throw error
      }

      return await response.json()
    },
    kakao: async () => {
      const response = await fetch.get(`${baseUrl}/kakao`, {
        options: { credentials: 'include' },
      })

      const data = await response.json()

      return data
    },
  }
}
