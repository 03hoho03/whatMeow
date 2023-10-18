import Navbar2 from '@/app/_components/Navbar2'
import BottomMenu from '@/app/_common/BottomMenu'
import React from 'react'

const layout = ({ children }: { children: React.ReactNode }) => (
  <div>
    <Navbar2 />
      {children}
    <BottomMenu />
  </div>
)

export default layout
