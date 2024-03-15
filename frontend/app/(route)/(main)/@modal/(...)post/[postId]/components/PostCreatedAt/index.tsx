'use client'
import calcDate from '@/app/_utils/calcDate'
import React from 'react'

interface PostCreatedAtProps {
  createdAt: Date
}

const PostCreatedAt = ({ createdAt }: PostCreatedAtProps) => {
  return <span>{`${calcDate(createdAt)}`}</span>
}

export default PostCreatedAt
