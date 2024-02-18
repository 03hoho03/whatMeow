import { useFetch } from '../_helpers/client/useFetch'
import { BASE_URL } from '../_utils/constants'

export interface CommentUploadApiResponse {
  success: boolean
}
interface Comment {
  commentId: number
  comment: string
  createdAt: string
  nickname: string
  thumnail: string
}

interface CommentService {
  upload: (comment: string, postId: number) => Promise<CommentUploadApiResponse>
  delete: (commentId: number) => Promise<{ success: boolean }>
  getList: (postId: number) => Promise<Comment[]>
}

function useCommentService(): CommentService {
  const fetch = useFetch()
  const baseUrl = `${BASE_URL}/api/v1/comment`
  return {
    upload: async (comment, postId) => {
      const body = {
        comment,
      }
      const response = await fetch.post(`${baseUrl}/${postId}`, {
        headers: {
          'Content-type': 'application/json',
        },
        body,
        options: {
          credentials: 'include',
        },
      })

      if (!response.ok) {
        throw new Error('오류가 발생하였습니다.')
      }

      return await response.json()
    },
    delete: async (commentId) => {
      const response = await fetch.delete(`${baseUrl}/${commentId}`, {
        options: { credentials: 'include' },
      })

      if (!response.ok) {
        throw new Error('오류가 발생하였습니다.')
      }

      return await response.json()
    },
    getList: async (postId) => {
      const response = await fetch.get(`${baseUrl}/${postId}`, {
        options: { credentials: 'include' },
      })

      if (!response.ok) {
        throw new Error('오류가 발생하였습니다.')
      }

      return await response.json()
    },
  }
}

export default useCommentService
