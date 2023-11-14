import { atom } from 'recoil'

export { hashtagList }

const hashtagList = atom<string[]>({
  key: 'hashtagList',
  default: [],
})
