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

socket.on('set_slide', function(set_slide_msg) {
    current_slide = set_slide_msg.new_slide
    document.getElementById("page_counter").innerText = current_slide
});

socket.on('connect', function() {
    socket.emit('add_me_to_room')
    document.getElementById("page_counter").innerText = current_slide
});