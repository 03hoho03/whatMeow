import './globals.css'
import '@fortawesome/fontawesome-svg-core/styles.css'
import { config } from '@fortawesome/fontawesome-svg-core'
import React from 'react'
import Recoil from './_store/Recoil'
import Providers from './_utils/provider' 

config.autoAddCss = false

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <Providers>
          <Recoil>
            {children}
            </Recoil>
        </Providers>
      </body>
    </html>
  )
}
