import React from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
// import { faUser } from '@fortawesome/free-solid-svg-icons'
import { faSquarePlus, faUser } from '@fortawesome/free-regular-svg-icons'
import Link from 'next/link'
import styled from './navbar.module.css'

// import style from './navbar.module.css'

function Navbar() {
  return (
    <div className={styled.main}>
      <button type="button">
        <img src="./bars.svg" alt="bars" className={styled.icons} />
      </button>
      <Link href="/">
        {/* <img src="./logo3.png" alt="왓냥" className={styled.logo} /> */}
        <img src="./logo2.svg" alt="왓냥" className={styled.logo} />
      </Link>
      <div className={styled.headerIcons}>
        <div className={styled.iconBtn}>
          <Link href="/writerForm">
            <FontAwesomeIcon icon={faSquarePlus} className={styled.icon} />
          </Link>
        </div>
        <div className={styled.iconBtn}>
          <Link href="/userProfile">
            <FontAwesomeIcon icon={faUser} className={styled.icon} />
          </Link>
        </div>
      </div>
    </div>
  )
}

export default Navbar
