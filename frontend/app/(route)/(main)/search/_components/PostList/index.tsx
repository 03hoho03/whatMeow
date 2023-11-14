'use client'

import React, { useRef } from 'react'
import {  useInfiniteQuery } from '@tanstack/react-query'
import axios from 'axios'
import { useObserver } from '@/app/_hooks/useUserObserver'
import style from './postList.module.css'

interface PokeMonItem {
  name:string,
  url:string,
}
const OFFSET = 30

const getPokemonList = ({ pageParam = 0 }) => {
  const response = axios
  .get("https://pokeapi.co/api/v2/pokemon", {
    params: {
      limit: OFFSET,
      offset: pageParam,
      },
  })
  .then(res => res?.data)
  console.log(response)
  return response
}
  
const PostList = () => {
  const bottom = useRef<HTMLDivElement | null>(null)
  const {
    data,
    status,
    error,
    fetchNextPage,
    hasNextPage,
    hasPreviousPage,
    isFetchingNextPage,
  } = useInfiniteQuery({
    queryKey:['pokemon'],
    queryFn: getPokemonList,
    initialPageParam: 0,
    getNextPageParam:(lastPage)=>{
      const { next } = lastPage
      if(!next) {
        return false;
      }
      const nextOffset = Number(new URL(next).searchParams.get("offset"))
      console.log(nextOffset)
      return nextOffset
    }
      
  })
  const onIntersect = ([entry]) => entry.isIntersecting && fetchNextPage()
  useObserver({
    target: bottom,
    onIntersect,
})
  return (
    <div>
      {status === "pending" && <p>불러오는 중</p>}
      {status === "error" && <p>{error.message}</p>}
      {status === "success" &&
        data.pages.map((group, index) => (
          <div key={index} className={style.card_list}>
            {group.results.map((pokemon:PokeMonItem,idx:number) => (
              <div key={`${pokemon.name}-${idx}`} className={style.card_wrapper}>
                <img
                  src={`https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${idx+1}.png`} 
                  alt={pokemon.name}
                />
              </div>
            ))}
          </div>
      ))}
      <button type='button' onClick={() => fetchNextPage()}>더 불러오기</button>
      <div ref={bottom} />
      {isFetchingNextPage && <p>계속 불러오는 중</p>}
    </div>
  )
}

export default PostList