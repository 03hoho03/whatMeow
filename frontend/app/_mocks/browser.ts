/* eslint-disable import/prefer-default-export */
import { setupWorker } from 'msw'
import handlers from './handler'

const worker = setupWorker(...handlers)
export { worker }
