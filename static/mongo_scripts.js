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
    socket.on('update', function(e) {
        console.log('update rxed')
        console.log(e)
        updateUIGameState(e)

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
    var updateUIGameState = function(game_data){
        var players = game_data.players
        var is_my_turn = false
        $('#deck_sz_lab').text(game_data.deck.length)
        $('#grave_yard_children').empty()
        for (var i = 0; i < game_data.grave_yard.length; i++){
            var lab = $('#grave_yard_lab').clone()
            lab.text(game_data.grave_yard[i])
            $('#grave_yard_children').append(lab)
        }
        $('#wait_for_children').empty()
        for (var i = 0; i < game_data.waiting_for.length; i++){
            if (game_data.waiting_for[i].user_name == user_name && game_data.waiting_for[i].kind =='turn'){
                is_my_turn = true
            }
            var lab = $('#wait_for_lab').clone()
            lab.text(game_data.waiting_for[i].user_name + ' ' + game_data.waiting_for[i].kind)
            $('#wait_for_children').append(lab)
        }
        for (var i = 0; i < players.length; i++){
            if (i == game_data.turn){
                $('#user_row'+i).removeClass('table-success')
                $('#user_row'+i).addClass('table-primary')
            }else if(players[i].user_name == user_name){
                $('#user_row'+i).removeClass('table-primary')
                $('#user_row'+i).addClass('table-success')
            }else{
                $('#user_row'+i).removeClass('table-primary')
            }
            $('#coins'+i).text(players[i].coins)
            for (var j = 0; j < 2; j++){
               if (j >= players[i].cards.length){
                   $('#card_'+players[i].user_name+'_'+j).empty()
               }else{
                   $('#card_'+players[i].user_name+'_'+j).text(players[i].cards[j])
               }
            }
        }
        if(is_my_turn){
            $('.turn_button').removeAttr('disabled')
        }else{
            $('.turn_button').attr('disabled', 'disabled')
        }
        var activity_log = game_data.action_log
        $("#act_list").empty()
        for (var i = activity_log.length - 1; i >= 0; i--){
            var s_act = activity_log[i]["user_name"] + " " + activity_log[i]["action"]
            if (i == activity_log.length -1){
                $('#latest_activity').text(s_act)
            }else{
                $('#act_list').append('<li class="list-group-item">'+s_act+'</li>')
            }
        }
        if("penalize" in game_data && game_data.penalize == user_name){
            $("#discardCardModal").modal('show')
        }
    }
});
