/* eslint-disable import/prefer-default-export */

'use client'

import { useState, type PropsWithChildren, useEffect } from 'react'

const isMockingMode = process.env.NEXT_PUBLIC_API_MOCKING === 'enabled'

function MSWComponent({ children }: PropsWithChildren) {
  const [mswReady, setMSWReady] = useState(() => !isMockingMode)

  useEffect(() => {
    const init = async () => {
      if (isMockingMode) {
        const initMocks = await import('@/app/_mocks/index').then(
          (res) => res.default,
        )
        await initMocks()
        setMSWReady(true)
      }
    }

    if (!mswReady) {
      init()
    }
  }, [mswReady])

  if (!mswReady) {
    return null
  }

  // eslint-disable-next-line react/jsx-no-useless-fragment
  return <>{children}</>
}

export { MSWComponent }
