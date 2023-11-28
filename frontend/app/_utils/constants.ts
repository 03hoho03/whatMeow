export { writer, BASE_URL, FEED_SIZE }

interface Writer {
  MAX_INPUT_LETTER: number
  MAX_HASHTAG_LETTER: number
}

const writer: Writer = {
  MAX_INPUT_LETTER: 500,
  MAX_HASHTAG_LETTER: 16,
}

const FEED_SIZE = 2

// process.env.NEXT_PUBLIC_DEV_BACKEND_URL
// process.env.NEXT_PUBLIC_DEV_BASE_URL
const BASE_URL =
  process.env.NODE_ENV === 'development'
    ? process.env.NEXT_PUBLIC_DEV_BACKEND_URL
    : process.env.NEXT_PUBLIC_BASE_URL
