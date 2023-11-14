'use client'

import React from 'react'
import { FaCheck } from 'react-icons/fa'

function TermForm() {
  return (
    <div>
      <div>
        <h3>이용약관 동의</h3>
      </div>
      <div>
        <div>
          <button id="checkAll" type="button">
            <FaCheck size={10} />
          </button>
          <label htmlFor="checkAll">전체 동의하기</label>
        </div>
        <div>
          <div>
            <div>
              <button id="term1" type="button">
                <FaCheck size={10} />
              </button>
              <label htmlFor="term1">(필수) 서비스 이용약관 동의</label>
            </div>
            <div>
              <button type="button">보기</button>
            </div>
            <div>
              <button id="term2" type="button">
                <FaCheck size={10} />
              </button>
              <label htmlFor="term2">(필수) 서비스 이용약관 동의</label>
            </div>
            <div>
              <button type="button">보기</button>
            </div>
          </div>
        </div>
      </div>
      <div>
        <button type="button">동의하고 시작하기</button>
      </div>
    </div>
  )
}

export default TermForm
