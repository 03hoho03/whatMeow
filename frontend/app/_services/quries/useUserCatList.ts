import { useQuery } from '@tanstack/react-query'
import useUserService from '../userService'

export const userCatListStateQueryKey = 'userCat'
export const useUserCatListQuery = () => {
  const userService = useUserService()
  const { data, isSuccess } = useQuery({
    queryKey: [userCatListStateQueryKey],
    queryFn: () => userService.getUserCat(),
  })

  return { data, isSuccess }
}
