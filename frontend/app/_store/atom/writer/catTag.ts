import { atom } from 'recoil'

export { catTagList }

interface CatInfo {
  id: number
  name: string
}

const catTagList = atom<CatInfo[]>({
  key: 'catTagList',
  default: [],
})
