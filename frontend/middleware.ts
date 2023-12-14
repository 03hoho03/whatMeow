import { NextResponse } from 'next/server'
import { NextRequest } from 'next/server'

const protectedRoutes = ['/feed']
const publicRoutes = ['/login', '/join']
// This function can be marked `async` if using `await` inside
// eslint-disable-next-line consistent-return
export async function middleware(request: NextRequest) {
  const accessToken = request.cookies.get('accessToken')?.value
  const currentPath = request.nextUrl.pathname
  const loginUrl =
    process.env.NODE_ENV === 'development'
      ? 'https://local.whatmeow.shop:3001/login'
      : 'https://www.whatmeow.shop/login'
  const homeUrl =
    process.env.NODE_ENV === 'development'
      ? 'https://local.whatmeow.shop:3001'
      : 'https://www.whatmeow.shop'

  console.log(currentPath)

  if (
    !accessToken &&
    protectedRoutes.some((route) => currentPath.includes(route))
  ) {
    return NextResponse.redirect(loginUrl)
  }

  const response = await fetch('https://api.whatmeow.shop/api/v1/user/cat', {
    headers: {
      Cookie: `accessToken=${accessToken}`,
    },
    credentials: 'include',
  })

  // 401 or 401 일 때 auth 가 필요한 라우트 접근 시
  if (
    !response.ok &&
    protectedRoutes.some((route) => currentPath.includes(route))
  ) {
    return NextResponse.redirect(loginUrl)
  }
  // 2xx 일 때 로그인 관련 라우트 접근 시
  if (
    response.ok &&
    publicRoutes.some((route) => currentPath.includes(route))
  ) {
    return NextResponse.redirect(homeUrl)
  }

  return NextResponse.next()
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
}
