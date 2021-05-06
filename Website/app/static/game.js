
const BG_COLOR = '#F5F5DC';

const gameScreen = document.querySelector('#gameScreen');

//Game Grid:
const startCord = 40;
const endCord = 760;
const littleBoxSize = 80;
const bigBoxSize = 240;

let canvas, ctx;

function init() {
	canvas = document.querySelector('#canvas');
	ctx = canvas.getContext('2d');

	canvas.width = canvas.height = 800;

	ctx.fillStyle = BG_COLOR;
	ctx.fillRect(0, 0, canvas.width, canvas.height);

	document.addEventListener('keydown', keydown)
	canvas.addEventListener('click', onCanvasClick)
}


function keydown(event) {
	console.log(event.keyCode)
	fetch('http://127.0.0.1:5000/api/test/')
		.then(res => res.json())
}

function onCanvasClick(event) {

	const [xCord, yCord] = getPosInCanvas(event);

	console.log(`x: ${xCord}`)
	console.log(`y: ${yCord}`)
}

function getPosInCanvas(event) {
	const rect = canvas.getBoundingClientRect();

	const x = event.clientX - rect.left;
	const y = event.clientY - rect.top;

	return [x, y]
}
function drawGrid(size, width) {



	ctx.strokeStyle = '#231f20';
	ctx.lineWidth = width;
	ctx.beginPath();
	// we don't want the very outsize boxes to have outside lines. This ain't sudoku!
	for (let i = startCord+size; i <= endCord-size; i += size) {
		ctx.moveTo(i, startCord);
		ctx.lineTo(i, endCord);
		ctx.moveTo(startCord, i);
		ctx.lineTo(endCord, i);
	}

	ctx.stroke();
}

init();

drawGrid(littleBoxSize, 3.0);
drawGrid(bigBoxSize, 7.0);