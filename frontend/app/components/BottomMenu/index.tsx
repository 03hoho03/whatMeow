import React from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import {
  faHouse,
  faClipboard,
  faMagnifyingGlass,
} from '@fortawesome/free-solid-svg-icons'
import { faBell, faUser } from '@fortawesome/free-regular-svg-icons'
import styled from './bottomMenu.module.css'

const userTools = () => (
  <div className={styled.main}>
    <button type="button">
      <FontAwesomeIcon icon={faHouse} className={styled.icon} />
    </button>
    <button type="button">
      <FontAwesomeIcon icon={faClipboard} className={styled.icon} />
    </button>
    <button type="button">
      <FontAwesomeIcon icon={faMagnifyingGlass} className={styled.icon} />
    </button>
    <button type="button">
      <FontAwesomeIcon icon={faBell} className={styled.icon} />
    </button>
    <button type="button">
      <FontAwesomeIcon icon={faUser} className={styled.icon} />
    </button>
  </div>
)

export default userTools
