/* eslint-disable import/prefer-default-export */
import { setupServer } from 'msw/node'
import handlers from './handler'

const server = setupServer(...handlers)
export { server }
