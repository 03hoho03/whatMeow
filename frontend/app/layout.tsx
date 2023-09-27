import './globals.css'
import '@fortawesome/fontawesome-svg-core/styles.css'
import { config } from '@fortawesome/fontawesome-svg-core'
import React from 'react'
import Navbar from './components/Navbar/index'
import BottomMenu from './components/BottomMenu/index'

config.autoAddCss = false

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <Navbar />
        <div className="main">{children}</div>
        <BottomMenu />
      </body>
    </html>
  )
}
