import { NextRequest, NextResponse } from 'next/server'

export async function GET(req: NextRequest) {
  const code = req.nextUrl.searchParams.get('code')

  if (code) {
    const body = {
      code,
    }
    const res = await fetch('http://127.0.0.1:7070/api/user/kakao', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    })
    if (res.status === 200) {
      const data = await res.json()

      const accessToken = data?.accessToken
      const refreshToken = data?.refreshToken

      const response = NextResponse.redirect('http://localhost:3000', {
        status: 302,
      })
      response.cookies.set({
        name: 'accessToken',
        value: accessToken,
        httpOnly: true,
      })
      response.cookies.set({
        name: 'refreshToken',
        value: refreshToken,
        httpOnly: true,
      })
      return response
    } else {
      return NextResponse.json({ status: 403 })
    }
  }
  return NextResponse.json({ status: 403 })
}
