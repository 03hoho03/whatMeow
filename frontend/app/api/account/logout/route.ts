import {cookies}from 'next/headers'

import { NextResponse } from 'next/server';

export async function GET() {
  const cookieStore = cookies();
  cookieStore.delete('accessToken');
  cookieStore.delete('refreshToken');
  return NextResponse
}
