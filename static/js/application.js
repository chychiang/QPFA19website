
$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var numbers_received = [];

    //retrieve data from server socket
    socket.on('data1', function(msg) {
        console.log("Received data1 " + msg.data);
        colorchanger('data1', msg.data, 'box1')
        $('#log').html(msg.data);
    });
    socket.on('data2', function(msg){
        console.log("Received data2 " + msg.data)
        colorchanger('data2', msg.data, 'box2')
        $('#log2').html(msg.data)
    });
});

function colorchanger(socketName, input, htmlElementId) {
    if (input == 'on') {
        document.getElementById(htmlElementId).style.backgroundColor = "rgba(255, 0, 0, 0.5)";
    }
    else if (input == "off") {
        document.getElementById(htmlElementId).style.backgroundColor = "rgba(0, 255, 0, 0.5)";
    }
    else {
        console.log("No data recieved from " + socketName);
    }
}