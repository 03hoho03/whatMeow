const calcDate = (createdAt: Date) => {
  const now = new Date()
  const diffInSeconds = Math.floor((now.getTime() - createdAt.getTime()) / 1000)

  if (diffInSeconds < 60) {
    return `${diffInSeconds} 초 전`
  } else if (diffInSeconds < 3600) {
    const diffInMinutes = Math.floor(diffInSeconds / 60)
    return `${diffInMinutes} 분 전`
  } else if (diffInSeconds < 86400) {
    const diffInHours = Math.floor(diffInSeconds / 3600)
    return `${diffInHours} 시간 전`
  } else if (diffInSeconds < 604800) {
    const diffInDays = Math.floor(diffInSeconds / 86400)
    return `${diffInDays} 일 전`
  } else {
    const year = createdAt.getFullYear()
    const month = createdAt.getMonth() + 1 // getMonth()는 0부터 시작
    const day = createdAt.getDate()
    const createdDate = `${year}.${month}.${day}`
    return createdDate
  }
}

export default calcDate
