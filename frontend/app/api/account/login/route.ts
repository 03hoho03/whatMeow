import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  const body = await request.json()
  const userData = JSON.stringify(body)
  try {
    const res = await fetch('http://127.0.0.1:7070/api/user/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: userData,
    })
    const data = await res.json()

    const accessToken = data?.accessToken
    const refreshToken = data?.refreshToken
    const user = data?.user

    const response = NextResponse.json({
      user,
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
  } catch (error) {
    console.log(error)
  }
}
