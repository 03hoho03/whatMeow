import { useRef, useState } from 'react'
import { useObserver } from '@/app/_hooks/useUserObserver'
import Link from 'next/link'
import style from './pokeCard.module.css'

const PostItem = ({ id, name }) => {
	const target = useRef(null) // 대상 ref
	const [visible, setVisible] = useState(false) // DOM을 렌더할 조건

    // isIntersecting의 경우에 DOM을 마운트 한다.
    const onIntersect = ([entry]) =>
    	entry.isIntersecting ? setVisible(true) : setVisible(false)

	useObserver({
		target,
		onIntersect,
		threshold: 0.1, // 화면 양끝에서 10%만 보여져도 onIntersect를 실행한다.
	})

	return (
		<Link href={`/pokemon/${id}`} key={id}>
			// 관측 대상인 target ref. Link는 Next.js의 가상 요소로 실체가 없기 때문에
			// a태그에 스타일과 ref를 줘야 한다.
			<a className={style.pokemon_item} ref={target} >
				// 리스트 안쪽 전부를 조건부로 비워 준다.
				{visible && (
					<>
						<img
							src={`https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${id}.png`}
							alt={name}
						/>
						<div className={style.item}>
							<div className={style.info_box}>
								<p className={style.label}>ID</p>
								<p className={style.info}>{id}</p>
							</div>
							<div className={style.info_box}>
								<p className={style.label}>name</p>
								<p className={style.info}>{name}</p>
							</div>
						</div>
					</>
				)}
			</a>
		</Link>
	)
}

export default PostItem