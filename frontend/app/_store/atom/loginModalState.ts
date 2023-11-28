import { atom } from 'recoil'

const loginModalState = atom<boolean>({
  key: 'loginModalState',
  default: false,
})

export default loginModalState
