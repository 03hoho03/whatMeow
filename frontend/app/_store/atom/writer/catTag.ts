import { atom } from 'recoil'

export { catTagList }

interface CatInfo {
  catId: number
  catName: string
}

const catTagList = atom<CatInfo[]>({
  key: 'catTagList',
  default: [],
})
