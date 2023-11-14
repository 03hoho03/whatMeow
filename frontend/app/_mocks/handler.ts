/* eslint-disable prettier/prettier */
/* eslint-disable implicit-arrow-linebreak */
import { rest } from 'msw'

export const MOCK_API_BASE_URL = 'http://localhost:3000';

const monthCatsData = [
  {
    url: './MonthlyCats/1.png',
    text: '3주 연속의 귀여움\n토리를 만나봐요',
  },
  {
    url: './MonthlyCats/2.png',
    text: '2주 연속의 귀여움\n토리를 만나봐요',
  },
  {
    url: './MonthlyCats/3.png',
    text: '1주 연속의 귀여움\n토리를 만나봐요',
  },
]

const handlers = [
  rest.get(`${MOCK_API_BASE_URL}/home`, async (req, res, ctx) => res(
    // ctx.status(200),
    ctx.json(
      monthCatsData,
    ),
  )),
]

// eslint-disable-next-line import/prefer-default-export
export default handlers
