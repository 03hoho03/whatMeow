import './globals.css'
import '@fortawesome/fontawesome-svg-core/styles.css'
import { config } from '@fortawesome/fontawesome-svg-core'
import React from 'react'
import BottomMenu from '@/app/_common/BottomMenu'
import Recoil from './_store/Recoil'

config.autoAddCss = false

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <Recoil>
          <div className="main">{children}</div>
          <BottomMenu />
        </Recoil>
      </body>
    </html>
  )
}
