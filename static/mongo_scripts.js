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
    $('.turn_button').on('click', function(e){
        action = $(e.target).data('action')
        if (action.length > 0){
            socket.emit('play action', {
                    action: action,
                    user_name: user_name,
                    room_name: room_name
            })
        }
    });
    $('.aux_button').on('click', function(e){
        action = $(e.target).data('action')
        if (action.length > 0){
            socket.emit('play action', {
                    action: action,
                    user_name: user_name,
                    room_name: room_name
            })
        }
    });
});
