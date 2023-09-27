// import cn from 'classnames'
import Carousel from './components/Carousel'
import style from './page.module.css'

export default function Home() {
  const monthCatsImages = ['./logo.svg', './logo2.svg', './cat.jpg']
  return (
    <div>
      <div className={style.month_cats}>
        <h3>이달의 고양이들</h3>
        <Carousel carouselList={monthCatsImages} autoPlay />
        <div className={style.month_cats_img_div}>
          <img src="./cat.jpg" alt="best-cat" />
        </div>
      </div>
    </div>
  )
}
