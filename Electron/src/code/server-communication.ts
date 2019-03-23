
//this will work on main process



console.log("PING;")

const net = require('net');
const port = 0;
const host = '127.0.0.1';

const server = net.createServer();
server.listen(port, host, () => {
    console.log("PORT:"+server.address().port+";");
});


let sockets: any = [];

server.on('connection', function(sock:any) {
    console.log('CONNECTED: ' + sock.remoteAddress + ':' + sock.remotePort);
    sockets.push(sock);

    sock.write("PING;");

    sock.on('data', function(data:any) {
        console.log('DATA ' + sock.remoteAddress + ': ' + data);
        // Write the data back to all the connected, the client will receive it as data from the server
        sockets.forEach(function(sock:any, index:any, array:any) {
            sock.write(sock.remoteAddress + ':' + sock.remotePort + " said " + data + '\n');
        });
    });

    sock.on('close', function(data:any) {
        let index = sockets.findIndex(function(o:any) {
            return o.remoteAddress === sock.remoteAddress && o.remotePort === sock.remotePort;
        })
        if (index !== -1) sockets.splice(index, 1);
        console.log('CLOSED: ' + sock.remoteAddress + ' ' + sock.remotePort);
    });
});