// import cn from 'classnames'
import BookMarkList from './_components/BookMarkList'
import MonthlyCats from './_components/MonthlyCats'
import Navbar2 from './_components/Navbar2'
import style from './page.module.css'

export default async function Home() {
  return (
    <div className={style.main}>
      <Navbar2 />
      <MonthlyCats />
      <BookMarkList />
    </div>
  )
}
