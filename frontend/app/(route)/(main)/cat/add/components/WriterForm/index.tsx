'use client'
import React from 'react'
import style from './writerForm.module.css'
import ImageUpload from '../ImageUpload'
import { useForm } from 'react-hook-form'
import { useRouter } from 'next/navigation'
import { useMutation } from '@tanstack/react-query'
import useCatService, {
  ProfileUploadApiResponse,
} from '@/app/_services/catService'

interface CatProfileSubmitFormResponse {
  thumnail: FileList
  name: string
  explain?: string
}
interface AddCatProfileApiResponse {
  catName: string
  explain: string | null
  gender: null
  breed: null
  ownerId: number
  id: number
}

const WriterForm = () => {
  const router = useRouter()
  const catService = useCatService()
  const {
    handleSubmit,
    register,
    formState: { errors },
  } = useForm<CatProfileSubmitFormResponse>()
  const profileMutation = useMutation<
    ProfileUploadApiResponse,
    Error,
    FormData
  >({
    mutationFn: (formData) => catService.profileUpload(formData),
  })

  const fields = {
    thumnail: register('thumnail', {
      required: '최소 1장 이상의 사진을 업로드 해주세요.',
    }),
    name: register('name', { required: '이름을 입력해주세요.' }),
    explain: register('explain', {
      maxLength: { value: 200, message: '200자 이하로 적어주세요.' },
    }),
  }

  const HandleProfileUpload = ({
    thumnail,
    name,
    explain,
  }: CatProfileSubmitFormResponse) => {
    const formData = new FormData()
    formData.append('file', thumnail[0])
    formData.append('catName', name)
    explain && formData.append('explain', explain)
    profileMutation.mutate(formData, {
      onSuccess: (response: AddCatProfileApiResponse) => {
        router.push(`/catprofile/${response.id}`)
      },
      onError: (error) => {
        console.log(error)
      },
    })
  }
  const HandleCancelUpload = () => {
    const isCancel = confirm(
      '정말로 취소하시겠습니까 ? 작성중이던 프로필은 저장되지않습니다.',
    )
    if (!isCancel) {
      return
    }
    router.push('/')
  }

  return (
    <form
      onSubmit={handleSubmit(HandleProfileUpload)}
      className={style.writerFormContainer}
    >
      <ImageUpload register={fields.thumnail} />
      <div className={style.inputContainer}>
        <h5>이름</h5>
        <input
          {...fields.name}
          className={style.writerInput}
          placeholder="고양이 이름을 입력해주세요."
        />
        <p className={style.errorMessage}>{errors?.name?.message}</p>
      </div>
      <div className={style.inputContainer}>
        <h5>소개</h5>
        <textarea
          {...fields.explain}
          className={style.writerInput}
          placeholder="200자 이내로 소개글을 입력해주세요."
        />
        <p className={style.errorMessage}>{errors?.explain?.message}</p>
      </div>
      <div className={style.submitBtnContainer}>
        <button className={style.submitBtn} type="submit">
          추가하기
        </button>
        <button
          className={style.cancelBtn}
          type="button"
          onClick={HandleCancelUpload}
        >
          취소하기
        </button>
      </div>
    </form>
  )
}

export default WriterForm
