'use client'
import Icon from '@/app/_common/Icon'
import Link from 'next/link'
import React from 'react'

interface BookMarkProps {
  info: BookMarkInfo
}
interface BookMarkInfo {
  title: string
  link: string
  type: string
}

const BookMark = ({ info: { title, link, type } }: BookMarkProps) => {
  return (
    <button type="button">
      <Link href={link}>
        <Icon type={type} />
        <span>{title}</span>
      </Link>
    </button>
  )
}

export default BookMark
