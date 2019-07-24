var ws = require('ws');
var websocket = require('websocket-stream');
var docker = require('../docker-browser-console');

var server = new ws.Server({
    port: 10000
});

// container_id = '50c916c2c6f9';
// var container = docker(container_id);
//if it is a remote container, do:
var remote_ip = '10.10.81.100';
var container_id = '387d914cee46';
container_id = process.argv[2]


var container = docker(container_id, {host: remote_ip});


/* Trying to open the browser automattically

var open = require('open');
var c = require('child_process');

var path = __dirname + '/index.html';
console.log(path);
var child_process = require("child_process"),
    url = __dirname + '/index.html';

if (process.platform == 'wind32') {

    cmd = 'start "%ProgramFiles%\Internet Explorer\iexplore.exe"';

} else if (process.platform == 'linux') {

    cmd = 'xdg-open';

} else if (process.platform == 'darwin') {

    cmd = 'open';

}

child_process.exec(cmd + ' "' + url + '"');

*/



server.on('connection', function(socket) {
    socket = websocket(socket);
    // this will spawn the container and forward the output to the browser
    //socket.pipe(docker('mafintosh/dev')).pipe(socket);
    socket.pipe(container).pipe(socket);
});
