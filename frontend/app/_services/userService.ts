import { useFetch } from '../_helpers/client/useFetch'

export { useUserService }

function useUserService(): IUserService {
  const fetch = useFetch()
  return {
    join: async (email, password, nickname) => {
      const response = await fetch.post('/api/account/join', {
        email,
        password,
        nickname,
      })
    },
    login: async (email, password) => {
      const response = await fetch.post('/api/account/login', {
        email,
        password,
      })
      return response.user.email
    },
    logout: async () => {
      await fetch.get('/api/account/logout')
    },
  }
}

interface IUserService {
  join: (email: string, password: string, nickname: string) => Promise<void>
  login: (username: string, password: string) => Promise<void>
  logout: () => Promise<void>
}
