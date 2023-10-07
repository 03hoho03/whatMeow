import './globals.css'
import '@fortawesome/fontawesome-svg-core/styles.css'
import { config } from '@fortawesome/fontawesome-svg-core'
import React from 'react'
import BottomMenu from '@/app/_common/BottomMenu'

config.autoAddCss = false

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <div className="main">{children}</div>
        <BottomMenu />
      </body>
    </html>
  )
}
