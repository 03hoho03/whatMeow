import { useQuery } from '@tanstack/react-query'
import { Like } from '../likeService'

export const LikeStateQueryKey = 'like'
export const useLikeQuery = (postId: number) => {
  const likeQuery = useQuery<Like>({
    queryKey: [LikeStateQueryKey, postId],
  })
  return { likeQuery }
}
