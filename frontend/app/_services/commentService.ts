import { useFetch } from '../_helpers/client/useFetch'
import { BASE_URL } from '../_utils/constants'

export interface CommentUploadApiResponse {
  success: boolean
}
interface CommentService {
  upload: (comment: string, postId: number) => Promise<CommentUploadApiResponse>
}

function useCommentService(): CommentService {
  const fetch = useFetch()
  const baseUrl = `${BASE_URL}/api/v1/comment`
  return {
    upload: async (comment, postId) => {
      const body = {
        comment,
      }
      const response = await fetch.post(
        `${baseUrl}/${postId}`,
        body,
        {
          'Content-type': 'application/json',
        },
        {
          credentials: 'include',
        },
      )
      if (!response.ok) {
        throw new Error('오류가 발생하였습니다.')
      }
      return await response.json()
    },
  }
}

export default useCommentService
