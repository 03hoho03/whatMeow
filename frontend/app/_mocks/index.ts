const initMockAPI = async (): Promise<void> => {
  if (typeof window === 'undefined') {
    const { server } = await import('@/app/_mocks/server')
    server.listen()
  } else {
    const { worker } = await import('@/app/_mocks/browser')
    worker.start()
  }
}

export default initMockAPI
