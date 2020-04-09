$(document).ready(function(){
    console.log('ready')
    console.log(room_name)
    var socket = io()
    socket.on('connect', function() {
        socket.emit('load play page', {
                data: 'Connected',
                user_name: user_name,
                room_name: room_name
        })
    });
    socket.on('update', function() {
        console.log('update rxed')
    });
    $('#takeincome').on('click', function(e){
        socket.emit('play action', {
                action: 'income',
                user_name: user_name,
                room_name: room_name
        })
    });
});
