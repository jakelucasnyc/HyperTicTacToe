
export function drawGrid(canvas, ctx, size, width) {

	const startCord = 40;
	const endCord = 760;


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

