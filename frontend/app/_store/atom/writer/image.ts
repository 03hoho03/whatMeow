import { atom } from 'recoil'

export { imagePreviewList, imageFileList }
export type { FileInfoType }

interface FileInfoType {
  url: string
  image: boolean
  video: boolean
  file: File
}

const imageFileList = atom<FileInfoType[]>({
  key: 'imageFileList',
  default: [],
})

const imagePreviewList = atom<string[]>({
  key: 'imagePreviewList',
  default: [],
})
