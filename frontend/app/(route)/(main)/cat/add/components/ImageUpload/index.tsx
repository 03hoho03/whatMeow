'use client'
import React from 'react'
import style from './imageUpload.module.css'
import { FileInfoType, imageFileList } from '@/app/_store/atom/writer/image'
import { useRecoilState } from 'recoil'
import { UseFormRegisterReturn } from 'react-hook-form'
import { CiCamera } from 'react-icons/ci'

interface ImageUploadProps {
  register: UseFormRegisterReturn
}

const ImageUpload = ({ register }: ImageUploadProps) => {
  const [fileList, setFileList] = useRecoilState<FileInfoType[]>(imageFileList)

  const HandleChangeFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const inputFileList = e.target.files

    if (!inputFileList) {
      return
    }

    const fileArray: FileInfoType[] = []
    const currentImageUrl = URL.createObjectURL(inputFileList[0])

    fileArray.push({
      url: currentImageUrl,
      image: inputFileList[0].type.includes('image'),
      video: inputFileList[0].type.includes('video'),
      file: inputFileList[0],
    })
    setFileList(fileArray)
  }
  return (
    <label htmlFor="imageUpload" className={style.uploadLabel}>
      {fileList.length > 0 ? (
        fileList.map(({ url }) => (
          <img
            key={url}
            alt="프로필 썸네일"
            src={url}
            className={style.profileThumnailImg}
          />
        ))
      ) : (
        <CiCamera size={64} />
      )}
      <input
        {...register}
        type="file"
        id="imageUpload"
        accept="image/*"
        onChange={HandleChangeFileInput}
        className={style.imageInput}
      />
    </label>
  )
}

export default ImageUpload
