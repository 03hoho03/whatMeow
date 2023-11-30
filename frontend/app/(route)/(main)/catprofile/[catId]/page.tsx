import React from 'react'
import style from './page.module.css'
import ProfileContainer from './components/ProfileContainer'

const CatProfile = ({ params }: { params: { catId: string } }) => {
  const intCatId = parseInt(params.catId)

  return (
    <div className={style.catProfilePageContainer}>
      <ProfileContainer catId={intCatId} />
    </div>
  )
}

export default CatProfile
