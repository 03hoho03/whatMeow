'use client'
import React from 'react'
import style from './uploadForm.module.css'
import ImageUpload from '../ImageUpload'
import { SubmitHandler, useForm } from 'react-hook-form'
import useAiService, { BreedAiApiResponse } from '@/app/_services/aiService'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { useSetRecoilState } from 'recoil'
import loginModalState from '@/app/_store/atom/loginModalState'

interface BreedAiSubmitFormReturn {
  file: FileList
}

const UploadForm = () => {
  const setLoginModal = useSetRecoilState(loginModalState)
  const aiService = useAiService()
  const queryClient = useQueryClient()
  const {
    register,
    handleSubmit,
    setError,
    formState: { errors },
  } = useForm<BreedAiSubmitFormReturn>()

  const { mutate } = useMutation<BreedAiApiResponse, Error, FormData>({
    mutationFn: (formData) => aiService.breedAi(formData),
  })

  const handleUploadImage: SubmitHandler<BreedAiSubmitFormReturn> = ({
    file,
  }) => {
    const formData = new FormData()
    formData.append('file', file[0])
    mutate(formData, {
      onSuccess: (data) => {
        console.log(data)
        queryClient.setQueryData(['breedAi'], data)
        queryClient.invalidateQueries({ queryKey: ['breedAi'] })
      },
      onError: (error) => {
        if (error.cause === 403 || error.cause === 401) {
          setLoginModal(true)
        } else if (error.cause === 422) {
          setError('root', {
            message: '고양이가 감지되지 않습니다. 다른 사진을 넣어주세요.',
          })
        }
      },
    })
  }

  return (
    <form
      onSubmit={handleSubmit(handleUploadImage)}
      className={style.uploadForm}
    >
      <ImageUpload register={register('file', { required: true })} />
      <button type="submit">묘종 알아보기</button>
      <p className={style.errorMessage}>{errors?.root?.message}</p>
    </form>
  )
}

export default UploadForm
