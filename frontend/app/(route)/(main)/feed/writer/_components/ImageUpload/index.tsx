'use client'

import React, { useRef } from 'react'
import { AiOutlineCamera } from 'react-icons/ai'
import { MdCancel } from 'react-icons/md'
import Swiper from '@/app/_common/Swiper'
import style from './imageUpload.module.css'
import { useRecoilState } from 'recoil'
import { FileInfoType, imageFileList } from '@/app/_store/atom/writer/image'

function ImageUpload() {
  const [fileList, setFileList] = useRecoilState<FileInfoType[]>(imageFileList)

  const swiperContainer = useRef<HTMLUListElement | null>(null)

  const HandleChangeFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const InputFileList = e.target.files

    if (!InputFileList) return
    if (fileList.length + InputFileList.length > 10) return

    const fileArray: FileInfoType[] = [...fileList]

    for (let i = 0; i < InputFileList.length; i += 1) {
      const currentImageUrl = URL.createObjectURL(InputFileList[i])
      fileArray.push({
        url: currentImageUrl,
        image: InputFileList[i].type.includes('image'),
        video: InputFileList[i].type.includes('video'),
        file: InputFileList[i],
      })
    }
    setFileList(fileArray)
  }
  const handleDeleteImage = (id: number) => {
    setFileList(fileList.filter((_, index) => index !== id))
  }

  return (
    <section className={style.main_wrapper}>
      <div className={style.upload_button}>
        <input
          id="imageUpload"
          accept="image/*,video/*"
          type="file"
          multiple
          className={style.upload_input}
          onChange={HandleChangeFileInput}
        />
        <label htmlFor="imageUpload" className={style.upload_label}>
          <AiOutlineCamera className={style.upload_img} />
          <p className={style.preview_length_container}>
            <span className={style.preview_length_now}>{fileList.length}</span>
            <span>/10</span>
          </p>
        </label>
      </div>
      <Swiper swiperContainer={swiperContainer}>
        <ul className={style.preview_ul} ref={swiperContainer}>
          {fileList.map(({ url }, idx) => (
            <li key={`${url}`} className={style.preview_li}>
              <img
                src={url}
                alt={`${url}+${idx}`}
                className={style.preview_img}
              />
              <button
                onClick={() => handleDeleteImage(idx)}
                type="button"
                className={style.preview_delete_btn}
              >
                <MdCancel className={style.delete_img} />
              </button>
            </li>
          ))}
        </ul>
      </Swiper>
    </section>
  )
}

export default ImageUpload
