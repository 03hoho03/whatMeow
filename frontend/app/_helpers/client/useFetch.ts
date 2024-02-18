/* eslint-disable @typescript-eslint/no-explicit-any */
export { useFetch }

interface RequestOptions {
  body?: any
  headers?: Record<string, string>
  options?: RequestInit
}

const useFetch = () => {
  return {
    get: request('GET'),
    post: request('POST'),
    put: request('PUT'),
    delete: request('DELETE'),
  }

  function request(method: string) {
    return (url: string, config?: RequestOptions) => {
      const requestOptions = {
        method,
        headers: {
          ...config?.headers,
        },
        ...config?.options,
      }

      if (config?.body) {
        if (method === 'POST') {
          if (config.body instanceof FormData) {
            requestOptions.body = config.body
          } else if (config.body instanceof Object) {
            requestOptions.body = JSON.stringify(config.body)
          }
        }
      }
      return fetch(url, requestOptions).then(handleResponse)
    }
  }

  async function handleResponse(response: Response) {
    if (!response.ok) {
      if (response.status === 401) {
        // 401 에 따른 accessToken refresh 로직 필요
        return response
      }
    }
    return response
  }
}
