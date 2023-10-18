import { cookies } from 'next/headers'
const baseUrl = 'http://127.0.0.1:7070'

export const fetchUserLogin = async (userData:any) => {
  await fetch(`${baseUrl}/api/user/login`,{
    method:'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body:userData
  })
}

export const fetchUserRefresh = async() => {
  const cookieStore = cookies();
  const accessToken = cookieStore.get('accessToken')?.value;
  const refreshToken = cookieStore.get('refreshToken')?.value;
  if(!accessToken || !refreshToken) {
    return;
  }
  const authorizationToken = `Bearer ${accessToken}`
  const response = await fetch(`${baseUrl}/api/user/refresh`,{
    method:"GET",
    headers: {
      'Content-Type': 'application/json',
      'Authorization':authorizationToken,
      'refresh':refreshToken,
    },
  })
  const data = await response.json()
  return data
}

export const fetchUserLogout = () => {
  const cookieStore = cookies();
  const result1 = cookieStore.delete('accessToken');
  console.log(result1)
  const result2 = cookieStore.delete('refreshToken')
  console.log(result2)
}
