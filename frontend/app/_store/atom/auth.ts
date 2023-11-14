import { atom } from 'recoil'
import { recoilPersist } from 'recoil-persist'

const { persistAtom } = recoilPersist({
  key: 'authState',
  storage: localStorage,
})

export { authState }

const authState = atom({
  key: 'authState',
  default: false,
  effects_UNSTABLE: [persistAtom],
})
