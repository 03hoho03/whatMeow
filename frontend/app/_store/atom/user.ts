import { atom } from 'recoil'
import { recoilPersist } from 'recoil-persist'

const { persistAtom } = recoilPersist({
  key: 'userAtom',
  storage: typeof window !== 'undefined' ? localStorage : undefined,
})

export { userAtom }

const userAtom = atom({
  key: 'userAtom',
  default: {
    user: null,
    isAuth: false,
  },
  effects_UNSTABLE: [persistAtom],
})
