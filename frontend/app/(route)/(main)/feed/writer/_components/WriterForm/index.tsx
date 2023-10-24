'use client'
import React from 'react'
import ImageUpload from '../ImageUpload'
import ContextForm from '../ContextForm'
import { SubmitHandler, useForm } from 'react-hook-form'
import HashTagForm from '../HashtagSection'
import { writer } from '@/app/_utils/constants'
import SubmitBtn from '@/app/_common/SubmitBtn'
import { useRecoilValue } from 'recoil'
import { imageFileList } from '@/app/_store/atom/writer/image'
import { hashtagList } from '@/app/_store/atom/writer/hashtag'
import { useFetch } from '@/app/_helpers/client/useFetch'

interface WriterFormValue {
  content: string
}

const WriterForm = () => {
  const fileList = useRecoilValue(imageFileList)
  const hashList = useRecoilValue(hashtagList)
  const fetch = useFetch()
  const {
    register,
    handleSubmit,
    watch,
    formState: { isValid },
  } = useForm<WriterFormValue>({ mode: 'onChange' })
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
    formData.append('tags', JSON.stringify(hashList))

    await fetch.post('/api/writer/submit', formData)
  }

  return (
    <form onSubmit={handleSubmit(SubmitSuccess)}>
      <ImageUpload />
      <ContextForm content={fields.content} watch={watch} />
      <HashTagForm />
      <SubmitBtn isValid={isValid}>
        <span>등록</span>
      </SubmitBtn>
    </form>
  )
}

export default WriterForm
