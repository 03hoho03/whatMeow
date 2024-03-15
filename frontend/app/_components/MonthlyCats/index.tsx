import React from 'react'
import Carousel from '../Carousel'

async function MonthlyCats() {
  const monthCatsData = [
    {
      url: './MonthlyCats/1.png',
      text: '3주 연속의 귀여움\n토리를 만나봐요',
    },
    {
      url: './MonthlyCats/2.png',
      text: '2주 연속의 귀여움\n토리를 만나봐요',
    },
    {
      url: './MonthlyCats/3.png',
      text: '1주 연속의 귀여움\n토리를 만나봐요',
    },
  ]

  return (
    <div>
      <Carousel carouselList={monthCatsData} />
    </div>
  )
}

export default MonthlyCats
