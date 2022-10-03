var socket = io();

function next_slide() {
    // update local counter
    current_slide++
    document.getElementById("page_counter").innerText = current_slide
    // update backend counter
    socket.emit('set_slide', {new_slide: current_slide})
}

function prev_slide() {
    // update local counter
    current_slide--
    document.getElementById("page_counter").innerText = current_slide
    // update backend counter
    socket.emit('set_slide', {new_slide: current_slide})
}