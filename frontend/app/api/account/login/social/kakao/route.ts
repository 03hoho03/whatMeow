import { NextResponse } from 'next/server'

export async function GET() {
  const RedirectUrl = `https://kauth.kakao.com/oauth/authorize?response_type=code&client_id=${process.env.KAKAO_CLIENT_ID}&redirect_uri=${process.env.KAKAO_REDIRECT_URL}`
  return NextResponse.redirect(RedirectUrl)
}
