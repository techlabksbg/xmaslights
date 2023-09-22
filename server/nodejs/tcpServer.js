// From https://riptutorial.com/node-js/example/22405/a-simple-tcp-server
// Include Nodejs' net module.
const net = require('net');
// The port on which the server is listening.
const port = 15878;

class Server {
    constructor() {
        // Create a new TCP server.
        this.clients = [];
        this.server = net.createServer((socket) => {
            // 'connection' listener.
            console.log('client connected');
            this.clients.push(socket);

            socket.on('end', () => {
                this.clients = this.clients.filter((c)=>c!==socket);
                console.log('client disconnected');
            });

            socket.on('data', function(chunk) {
                let s = data.toString();
                if (s=="ping") {
                    console.log("pong!");
                    socket.write("pong");
                    return;
                }
                console.log("received: ")
                console.log(s);
            });

            socket.on('error', function(err) {
                console.log(`Error: ${err}`);
                socket.clos
            });

        });

        // The server listens to a socket for a client to make a connection request.
        // Think of a socket as an end point.
        server.listen(port, function() {
            console.log(`Server listening for connection requests on socket localhost:${port}`);
        });
    }
    send(data){
        this.clients.forEach((c)=>c.write(data));
    }
}
