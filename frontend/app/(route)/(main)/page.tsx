import BookMarkList from '../../_components/BookMarkList'
import MonthlyCats from '../../_components/MonthlyCats'
import style from './page.module.css'

export default async function Home() {
  return (
    <div className={style.main}>
      <MonthlyCats />
      <BookMarkList />
    </div>
  )
}
