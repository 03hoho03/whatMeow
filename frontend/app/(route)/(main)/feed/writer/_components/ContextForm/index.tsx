import React from 'react'
import style from './contextForm.module.css'
import cn from 'classnames'
import { UseFormRegisterReturn, UseFormWatch } from 'react-hook-form'
import { writer } from '@/app/_utils/constants'

interface ContextFormProps {
  content: UseFormRegisterReturn<string>
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  watch: UseFormWatch<any>
}

function ContextForm({ content, watch }: ContextFormProps) {
  const countCharacters = () => {
    const content = watch('content')
    if (!content) {
      return 0
    }
    return content.length
  }
  return (
    <section className={style.main_wrapper}>
      <h3 className={style.form_title}>내용</h3>
      <div className={style.textarea_wrapper}>
        <textarea
          {...content}
          className={style.form_textarea}
          maxLength={writer.MAX_INPUT_LETTER}
        />
        <div className={style.form_letter_div}>
          <span
            className={cn({
              [style.form_letter_max]:
                countCharacters() >= writer.MAX_INPUT_LETTER,
            })}
          >
            {countCharacters()}
          </span>
          <span>{`/${writer.MAX_INPUT_LETTER}`}</span>
        </div>
      </div>
    </section>
  )
}

export default ContextForm
