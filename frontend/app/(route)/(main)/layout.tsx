import Navbar from '@/app/_components/Navbar'
import BottomMenu from '@/app/_common/BottomMenu'
import React from 'react'

const layout = ({
  children,
  modal,
}: {
  children: React.ReactNode
  modal: React.ReactNode
}) => (
  <div>
    <Navbar />
    {children}
    {modal}
    <BottomMenu />
  </div>
)

export default layout
