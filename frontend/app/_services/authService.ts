import { useSetRecoilState } from 'recoil'
import { useFetch } from '../_helpers/client/useFetch'
import { userAtom } from '../_store/atom/user'
import { BASE_URL } from '../_utils/constants'

export { useAuthService }

interface LoginApiResponse {}
interface AuthSerivce {
  register: (email: string, password: string, username: string) => Promise<void>
  login: (username: string, password: string) => Promise<void>
  logout: () => Promise<void>
}

function useAuthService(): AuthSerivce {
  const setUser = useSetRecoilState(userAtom)
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
      try {
        await fetch.get('/api/account/logout')
        setUser({
          user: null,
          isAuth: false,
        })
      } catch (error) {
        console.log(error)
      }
    },
  }
}
