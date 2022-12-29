const connect = (message) => {
    let socket = new WebSocket('ws://localhost:8000');

    socket.addEventListener('open', function (event) {
        if (message) {
            socket.send(message)
        } else {
            socket.send('Connection Established');
        }
    });

    socket.addEventListener('message', function (event) {
        console.log(event.data);
        result.textContent = event.data
    });

    socket.addEventListener('close', (e) => {
        console.log('Socket is closed.', e.reason);
        result.textContent = result.textContent + ' Socket is closed.'
    })
}

connect()

btnSend.addEventListener('click', (e) => {
    connect("Click button");
})