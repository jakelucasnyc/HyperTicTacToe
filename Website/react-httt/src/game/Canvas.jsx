import React, { useRef, useEffect } from 'react'
import { drawGrid } from './canvasDraw.js'


export default class Canvas extends React.Component {

	static BG_COLOR = '#F5F5DC';
	static startCord = 40;
	static endCord = 760;
	static littleBoxSize = 80;
	static bigBoxSize = 240;

	constructor(props) {
		super(props)
		this.state = { 
			x: 0, 
			y: 0, 
			moves: '',
			board: [
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0]
			],

		};
		this.getClickCords = this.getClickCords.bind(this);
		this.canvasRef = React.createRef();


	}

	componentDidMount() {

		this.canvas = this.canvasRef.current;
		this.ctx = this.canvas.getContext('2d');
		this.canvas.width = this.canvas.height = 800;

		this.ctx.fillStyle = Canvas.BG_COLOR;
		this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

		drawGrid(this.canvas, this.ctx, Canvas.littleBoxSize, 3.0);
		drawGrid(this.canvas, this.ctx, Canvas.bigBoxSize, 7.0)

	}

	componentDidUpdate(prevProps, prevState) {

		//if the user is clicking on the same spot over and over again
		if (this.state.x === prevState.x & this.state.y === prevState.y) {return}
			
		console.log(`${this.state.x}, ${this.state.y}`)
		console.log(`${prevState.x}, ${prevState.y}`)


	}

	// useCanvas() {
	// 	return [this.state, this.canvas, this.ctx]
		
	// }

	getClickCords(event) {

		const rect = this.canvas.getBoundingClientRect();

		const x = event.clientX - rect.left;
		const y = event.clientY - rect.top;

		this.setState((state, props) => {
			return {x: x, y: y}
		});
	} 

	render() {
		return (
			<canvas ref={this.canvasRef} onClick={this.getClickCords} {...this.props}/>
		)
	}
}