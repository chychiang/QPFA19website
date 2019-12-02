$(document).ready(function(){
    //connect to the socket server once the document is ready
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    
    //retrieve data from server socket
    socket.on('data1', function(msg) {
        console.log("Received data1 " + msg.data);
        colorchanger('data1', msg.data, 'box1')
        $('#log').html(msg.data);
        $('#time1').html(msg.time);
    });
    socket.on('data2', function(msg){
        console.log("Received data2 " + msg.data)
        colorchanger('data2', msg.data, 'box2')
        $('#log2').html(msg.data)
        $('#time2').html(msg.time)
    });
});

function colorchanger(socketName, input, htmlElementId) {
    /*  intuitive visuals of the availability of the laundry machines
        unavailable machines have red background
        available machines have green background */
    if (input == 'Unavailable') {
        document.getElementById(htmlElementId).style.backgroundColor = "rgba(255, 0, 0, 0.5)";
    }
    else if (input == "Available") {
        document.getElementById(htmlElementId).style.backgroundColor = "rgba(0, 255, 0, 0.5)";
    }
    else {
        //for debug
        console.log("No data recieved from " + socketName);
    }
}