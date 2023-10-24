export { writer, BASE_URL }

interface Writer {
  MAX_INPUT_LETTER: number
  MAX_HASHTAG_LETTER: number
}

const writer: Writer = {
  MAX_INPUT_LETTER: 500,
  MAX_HASHTAG_LETTER: 16,
}

const BASE_URL =
  process.env.NODE_ENV === 'development'
    ? process.env.BASE_URL
    : 'http://localhost:7070'
