import Navbar from '@/app/_components/Navbar'
import BottomMenu from '@/app/_common/BottomMenu'
import React from 'react'

const layout = ({ children }: { children: React.ReactNode }) => (
  <div>
    <Navbar />
    {children}
    <BottomMenu />
  </div>
)

export default layout
