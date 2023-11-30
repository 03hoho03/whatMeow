'use client'
import React from 'react'
import style from './profileContainer.module.css'
import Profile from '../Profile'
import PostList from '../PostList'
import { useQuery } from '@tanstack/react-query'
import useCatService from '@/app/_services/catService'

const ProfileContainer = ({ catId }: { catId: number }) => {
  const catService = useCatService()
  const { data } = useQuery({
    queryKey: ['hydrate-catProfile', catId],
    queryFn: () => catService.getCatProfile(catId),
  })

  return (
    <div className={style.catProfileContainer}>
      {data ? (
        <>
          <Profile
            explain={data.explain}
            thumnail={data.image}
            catName={data.name}
          />
          <PostList posts={data.posts} />
        </>
      ) : (
        <>로딩중...</>
      )}
    </div>
  )
}

export default ProfileContainer
