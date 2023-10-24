import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  const formData = await request.formData()
  const file = await formData.getAll('files')
  const content = await formData.get('content')
  const tags = await formData.get('tags')
  console.log(file, content, tags)
  const response = NextResponse.json({ status: 200 })
  return response
}
