import React from 'react'
import { FcCameraIdentification, FcTodoList } from 'react-icons/fc'
import { SiEventbrite } from 'react-icons/si'

interface IconProps {
  type: string
}
const Icon = ({ type }: IconProps) => {
  return type === 'camera' ? (
    <FcCameraIdentification />
  ) : type === 'test' ? (
    <FcTodoList />
  ) : type === 'event' ? (
    <SiEventbrite />
  ) : type === 'another' ? (
    <SiEventbrite />
  ) : (
    <></>
  )
}

export default Icon
