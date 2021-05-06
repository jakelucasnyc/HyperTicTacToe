import React, { useState, useEffect } from 'react';
import Canvas from './Canvas'


export default function Game() {


		let initialGameData = {
		moves: '',
		xResign: false,
		oResign: false,
		xDraw: false,
		oDraw: false,
		
	}

	const [gameData, updateGameData] = useState(initialGameData)
	const [mousePos, updateMousePos] = useState([0, 0])

	// useEffect(() => {
	// 	console.log(mousePos);

	// }, [mousePos])


	return (
		<section className="vh-100">
			<div className="container h-100">
				<div id="gameScreen" className="h-100">
					<div className="d-flex flex-column align-items-center justify-content-center h-100">
						<Canvas id="gameCanvas"/>
					</div>
				</div>
			</div>
		</section>

	)
}