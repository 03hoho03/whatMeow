import { useQuery } from '@tanstack/react-query'

interface LikeState {
  count: number
  isLike: boolean
}

export const LikeStateQueryKey = 'like'
export const useLikeQuery = (postId: number) => {
  const likeQuery = useQuery<LikeState>({
    queryKey: [LikeStateQueryKey, postId],
  })
  return { likeQuery }
}
