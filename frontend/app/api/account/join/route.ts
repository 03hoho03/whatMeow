import { NextResponse } from 'next/server';

export async function POST(request:Request) {
  const body = await request.json()
  const userData = JSON.stringify(body);
  try {
    // const res = await fetch('http://127.0.0.1:7070/api/user/register',{
    //   method: 'POST',
    //   headers: {
    //     'Content-Type' : 'application/json',
    //   },
    //   body:userData,
    // })
    // const data = await res.json();
    // console.log(data);
    return NextResponse.json({
      status:201
    })
  } catch(error) {
    console.log('played');
    console.log(error)
  }
}