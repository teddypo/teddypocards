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
            if (game_data.waiting_for[i].user_name == user_name && game_data.waiting_for[i].kind == 'discard'){
                // youve been assassinated or infected or lost a challenge
                for (var j = game_data.action_log.length - 1; j >= 0; j--){
                    var doer = game_data.action_log[j]['user_name']
                    if (game_data["action_log"][j]['action'].startsWith('assassinate')){
                        // It was an assassination
                        $('#modal_header_text').text('Assassinated')
                        $('#modal_body_text').text("You've been assassinated by "+doer+". You must block, challenge, or choose a card to discard")
                        $('#modal_challenge').removeClass('d-none')
                        $('#modal_block').removeClass('d-none')
                        var my_cards = players.filter(player => player.user_name == user_name)[0].cards
                        for (var k = 0; k < 4; k++){
                            if (k < my_cards.length){
                                $('#modal_discard'+k).text('Discard ' + my_cards[k])
                                $('#modal_discard' + k).removeClass('d-none')
                            }else{
                                $('#modal_discard'+k).empty()
                                $('#modal_discard' + k).addClass('d-none')
                            }
                        }
                        $('#modal_reveal0').addClass('d-none')
                        $('#modal_reveal1').addClass('d-none')
                        $('#discardCardModal').modal('show')
                        break;
                    }
                    if (game_data["action_log"][j]['action'].startsWith('infect')){
                        // It was an infect
                        $('#modal_header_text').text('Infected')
                        $('#modal_body_text').text("You've been infected by "+doer+". Which cant be blocked or challenged. Choose a card to discard")
                        $('#modal_challenge').addClass('d-none')
                        $('#modal_block').addClass('d-none')
                        var my_cards = players.filter(player => player.user_name == user_name)[0].cards
                        for (var k = 0; k < 4; k++){
                            if (k < my_cards.length){
                                $('#modal_discard'+k).text('Discard ' + my_cards[k])
                                $('#modal_discard' + k).removeClass('d-none')
                            }else{
                                $('#modal_discard'+k).empty()
                                $('#modal_discard' + k).addClass('d-none')
                            }
                        }
                        $('#modal_reveal0').addClass('d-none')
                        $('#modal_reveal1').addClass('d-none')
                        $('#discardCardModal').modal('show')
                        break;
                    }
                    if (game_data["action_log"][j]['action'] == "challenge"){
                        // You've lost a challenge
                        $('#modal_header_text').text('Challenge Failed')
                        $('#modal_body_text').text("Your challenge failed, choose a card to send to the graveyard")
                        $('#modal_challenge').addClass('d-none')
                        $('#modal_block').addClass('d-none')
                        var my_cards = players.filter(player => player.user_name == user_name)[0].cards
                        for (var k = 0; k < 4; k++){
                            if (k < my_cards.length){
                                $('#modal_discard'+k).text('Discard ' + my_cards[k])
                                $('#modal_discard' + k).removeClass('d-none')
                            }else{
                                $('#modal_discard'+k).empty()
                                $('#modal_discard' + k).addClass('d-none')
                            }
                        }
                        $('#modal_reveal0').addClass('d-none')
                        $('#modal_reveal1').addClass('d-none')
                        $('#discardCardModal').modal('show')
                        break;
                    }
                }
            }
            if (game_data.waiting_for[i].user_name == user_name && game_data.waiting_for[i].kind == 'doublediscard' && ! $('#discardCardModal').hasClass('show')){
                // you gotta finish your exchange
                $('#modal_header_text').text('Exchange')
                $('#modal_body_text').text("You've elected to exchange. Select two cards to return to the deck")
                $('#modal_challenge').addClass('d-none')
                $('#modal_block').addClass('d-none')
                var my_cards = players.filter(player => player.user_name == user_name)[0].cards
                for (var k = 0; k < 4; k++){
                    if (k < my_cards.length){
                        $('#modal_discard'+k).text('Discard ' + my_cards[k])
                        $('#modal_discard' + k).removeClass('d-none')
                    }else{
                        $('#modal_discard'+k).empty()
                        $('#modal_discard' + k).addClass('d-none')
                    }
                }
                $('#modal_reveal0').addClass('d-none')
                $('#modal_reveal1').addClass('d-none')
                var cards_clicked = []
                $('[id^=modal_discard]').on('click', function(e){
                        $(e.target).addClass('d-none')
                        cards_clicked.push($(e.target).data('index'))
                        if(cards_clicked.length < 2){
                            e.stopPropagation()
                        }else{
                            action = 'doublediscard' + cards_clicked[0] + '_' + cards_clicked[1];
                            socket.emit('play action', {
                                action: action,
                                user_name: user_name,
                                room_name: room_name
                            })
                        }
                });
                $('#discardCardModal').modal('show')
            }
            if (game_data.waiting_for[i].user_name == user_name && game_data.waiting_for[i].kind == 'reveal'){
                // you've been challenged
                var log = game_data["action_log"]
                var was_exchange = false
                for (var j = log.length - 1; i >= 0; j--){
                    if (log[j].action == 'exchange'){
                        was_exchange = true;
                        break;
                    }
                    if ( ! log[j].action.startsWith('doublediscard') &&
                         ! log[j].action.startsWith('allow') &&
                         ! log[j].action.startsWith('challenge')){
                        // these are the only things that could have happened between now and the exchange
                        break
                    }
                }
                $('#modal_header_text').text('Challenged')
                $('#modal_body_text').text("You've been challanged. You must choose a card to reveal")
                $('#modal_challenge').addClass('d-none')
                $('#modal_block').addClass('d-none')
                $('#modal_discard0').addClass('d-none')
                $('#modal_discard1').addClass('d-none')
                $('#modal_discard2').addClass('d-none')
                $('#modal_discard3').addClass('d-none')
                var my_cards = players.filter(player => player.user_name == user_name)[0].cards
                console.log(was_exchange)
                if (was_exchange){
                    my_cards = game_data["pre_exchange_cards"]
                }
                for (var k = 0; k < 2; k++){
                    if (k < my_cards.length){
                        $('#modal_reveal'+k).text('Reveal ' + my_cards[k])
                        $('#modal_reveal' + k).removeClass('d-none')
                    }else{
                        $('#modal_reveal'+k).empty()
                        $('#modal_reveal' + k).addClass('d-none')
                    }
                }
                $('#discardCardModal').modal('show')
            }
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
