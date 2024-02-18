import { useMutation } from '@tanstack/react-query'
import { useAuthService } from '../authService'

interface LoginMutationVariables {
  email: string
  password: string
}

export const useLoginMutation = () => {
  const authService = useAuthService()
  const loginMutation = useMutation<void, Error, LoginMutationVariables>({
    mutationFn: ({ email, password }) => authService.login(email, password),
  })

  return { loginMutation }
}
