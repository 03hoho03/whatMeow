'use client'
import React from 'react'
import ImageUpload from '../ImageUpload'
import ContextForm from '../ContextForm'
import { SubmitHandler, useForm } from 'react-hook-form'
import HashtagSection from '../HashtagSection'
import CatTagSection from '../CatTagSection'
import { writer } from '@/app/_utils/constants'
import SubmitBtn from '@/app/_common/SubmitBtn'
import { useRecoilValue } from 'recoil'
import { imageFileList } from '@/app/_store/atom/writer/image'
import { hashtagList } from '@/app/_store/atom/writer/hashtag'
import { useFeedService } from '@/app/_services/feedService'
import { useMutation } from '@tanstack/react-query'
import { useRouter } from 'next/navigation'
import { catTagList } from '@/app/_store/atom/writer/catTag'

interface WriterFormValue {
  content: string
}

const WriterForm = () => {
  const route = useRouter()
  const fileList = useRecoilValue(imageFileList)
  const hashList = useRecoilValue(hashtagList)
  const catTag = useRecoilValue(catTagList)
  const feedService = useFeedService()
  const {
    register,
    handleSubmit,
    watch,
    formState: { isValid },
  } = useForm<WriterFormValue>({ mode: 'onChange' })
  const { mutate } = useMutation({
    mutationFn: (form: FormData) => feedService.upload(form),
    onSuccess: () => {
      route.push('/')
    },
    onError: (error) => {
      // status 따른 분기 처리 예정
      console.log(error)
    },
  })

  const fields = {
    content: register('content', {
      required: '',
      maxLength: {
        value: writer.MAX_INPUT_LETTER,
        message: `최대 ${writer.MAX_INPUT_LETTER}자 까지 입력 가능합니다.`,
      },
    }),
  }
  const SubmitSuccess: SubmitHandler<WriterFormValue> = async ({
    content,
  }: {
    content: string
  }) => {
    if (fileList.length === 0 || !isValid) {
      return
    }
    const formData = new FormData()
    fileList.forEach(({ file }) => {
      formData.append('files', file)
    })
    formData.append('content', content)
    catTag.forEach((tag) => formData.append('cat_ids', tag.id.toString()))
    hashList.forEach((tag) => formData.append('tags', tag))

    mutate(formData)
    // await feedService.upload(formData)
  }

  return (
    <form onSubmit={handleSubmit(SubmitSuccess)}>
      <ImageUpload />
      <ContextForm content={fields.content} watch={watch} />
      <CatTagSection />
      <HashtagSection />
      <SubmitBtn isValid={isValid}>
        <span>등록</span>
      </SubmitBtn>
    </form>
  )
}

export default WriterForm
