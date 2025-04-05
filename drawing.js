// Get the canvas element and its context
const canvas = document.getElementById('circleCanvas');
const ctx = canvas.getContext('2d');

// Set canvas size to match window dimensions
function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

// Initial sizing
resizeCanvas();

// Resize canvas when window size changes
window.addEventListener('resize', function() {
    resizeCanvas();
    drawCircuit();
});

// Circle properties
const circle = {
    x: canvas.width / 2,
    y: canvas.height / 2,
    radius: 80,
    color: '#808080', // Start with grey
    isYellow: false
};

// Function to draw the circle
function drawCircle() {
    // Clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw the circle
    ctx.beginPath();
    ctx.arc(circle.x, circle.y, circle.radius, 0, Math.PI * 2);
    ctx.fillStyle = circle.color;
    ctx.fill();
    ctx.closePath();
}

// Draw the circle initially
//drawCircle();

// Handle click events
//canvas.addEventListener('click', function(event) {
//    // Get mouse position relative to canvas
//    const rect = canvas.getBoundingClientRect();
//    const mouseX = event.clientX - rect.left;
//    const mouseY = event.clientY - rect.top;
//
//    // Check if click is inside circle
//    const distance = Math.sqrt(
//        Math.pow(mouseX - circle.x, 2) +
//        Math.pow(mouseY - circle.y, 2)
//    );
//
//    // If click is inside circle, toggle color
//    if (distance <= circle.radius) {
//        circle.isYellow = !circle.isYellow;
//        circle.color = circle.isYellow ? '#FFFF00' : '#808080';
//        drawCircle();
//    }
//});

// Circuit properties
//const circuit = {
//    switchState: true,
//    x: 20,
//    y: 100,
//};

// Function to draw the circuit
function drawSwitch(circuit) {

    // Set line properties
    ctx.lineWidth = 3;
    //ctx.lineCap = 'round';
    //ctx.lineJoin = 'round';
    //ctx.strokeStyle = '#000';

    // Move the the base position where the switch will be placed
    ctx.save();  // 0
    ctx.translate(circuit.x, circuit.y);

    // We know the max height of the switch, so we can clear the canvas.
    const maxHeight = 52.5;  // 100 * sin(30deg), plus some margin
    ctx.clearRect(0, -maxHeight, 300, maxHeight + 5);

    // Start building a path
    ctx.beginPath();

    // Draw a horizontal line
    ctx.moveTo(0, 0);
    ctx.lineTo(100, 0);

    // Now, we will draw a line for the switch.
    // We translate the origin to the end of previous line and then rotate
    // the reference frame. We restore afterwards.
    const angleDegrees = circuit.isOpen ? 30 : 0;
    ctx.translate(100, 0);
    ctx.save();  // 1
    ctx.rotate(-angleDegrees * Math.PI / 180);
    ctx.lineTo(100, 0);
    ctx.restore();  // 1

    // The previous origin is left at the end of the first horizontal line.
    // We move to the start of the right line, then draw another horizontal line.
    ctx.translate(100, 0);
    ctx.moveTo(0, 0);
    ctx.lineTo(100, 0);

    ctx.restore(); // 0

    // Finally, we draw the line
    ctx.stroke();
}

// Draw the switches
// Do each twice to ensure they canvas is cleared
drawSwitch({
    x: 20,
    y: 100,
    isOpen: true,
});
drawSwitch({
    x: 20,
    y: 100,
    isOpen: false,
});
drawSwitch({
    x: 20,
    y: 200,
    isOpen: false,
});
drawSwitch({
    x: 20,
    y: 200,
    isOpen: true,
});
drawSwitch({
    x: 20,
    y: 300,
    isOpen: true,
});
drawSwitch({
    x: 20,
    y: 300,
    isOpen: false,
});

//// Handle click events for the switch
//canvas.addEventListener('click', function(event) {
//    // Get mouse position relative to canvas
//    const rect = canvas.getBoundingClientRect();
//    const mouseX = event.clientX - rect.left;
//    const mouseY = event.clientY - rect.top;
//
//    // Check if click is near the switch
//    if (mouseX >= circuit.switchX - circuit.switchWidth/2 - 10 &&
//        mouseX <= circuit.switchX + circuit.switchWidth/2 + 10 &&
//        mouseY >= circuit.switchY - circuit.switchHeight/2 - 10 &&
//        mouseY <= circuit.switchY + circuit.switchHeight/2 + 10) {
//
//        // Toggle switch state
//        circuit.switchState = !circuit.switchState;
//
//        // Redraw the circuit
//        drawCircuit();
//    }
//});
