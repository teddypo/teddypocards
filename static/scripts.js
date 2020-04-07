var exchange_count = 0

$(document).ready(function(){
	$('#create_form').submit(function(e){
		// add some form validation and preventDefault here?
	});
	$('#exchangeDropWrap').on('show.bs.dropdown', function(){
		$('#exchangeDropContent').append('<a class="dropdown-item" href="#" id="exchangeCard1">Discard RandCard</a>')
		$('#exchangeDropContent').append('<a class="dropdown-item" href="#" id="exchangeCard1">Discard RandCard</a>')
		$('#exchangeDropContent').append('<a class="dropdown-item" href="#" id="exchangeCard1">Discard RandCard</a>')
		$('#exchangeDropContent').append('<a class="dropdown-item" href="#" id="exchangeCard1">Discard RandCard</a>')
		$('[id^=exchangeCard]').on('click', function(){
			this.remove()
			exchange_count++;
			if (exchange_count >= 2){
				console.log('click')
				$('#exchangeDropWrap').dropdown('hide')
				exchange_count = 0;
				$('#exchangeDropContent').empty()
			}
		});
	});
	$('#exchangeDropWrap').on('hide.bs.dropdown', function(e){
		if (exchange_count > 0){
			e.preventDefault()
		}
	});
	$('#takeincome').on('click', function(e){
            $.ajax({
                url: '/action/'+user_name+'/takeincome/'+game_name,
                data: '{}',
                success: function(result){
                    console.log(result)
                    updateUIGameState(result.game_data)
                }
            });
	});
	$('#takeforeignaid').on('click', function(e){
            $.ajax({
                url: '/action/'+user_name+'/takeforeignaid/'+game_name,
                data: '{}',
                success: function(result){
                    console.log(result)
                    updateUIGameState(result.game_data)
                }
            });
	});
	$('#block_button').on('click', function(e){
            $.ajax({
                url: '/action/'+user_name+'/block/'+game_name,
                data: 'desired_block='+$("#latest_activity").text(),
                success: function(result){
                    console.log(result)
                    updateUIGameState(result.game_data)
                }
            });
	});
	$('#challenge_button').on('click', function(e){
            $.ajax({
                url: '/action/'+user_name+'/challenge/'+game_name,
                data: 'desired_challenge='+$("#latest_activity").text(),
                success: function(result){
                    console.log(result)
                    updateUIGameState(result.game_data)
                }
            });
	});
	$('#discard0').on('click', function(e){
            $.ajax({
                url: '/action/'+user_name+'/discard_0/'+game_name,
                data: 'desired_challenge='+$("#latest_activity").text(),
                success: function(result){
                    console.log(result)
                    updateUIGameState(result.game_data)
                }
            });
	});
	$('#discard1').on('click', function(e){
            $.ajax({
                url: '/action/'+user_name+'/discard_1/'+game_name,
                data: 'desired_challenge='+$("#latest_activity").text(),
                success: function(result){
                    console.log(result)
                    updateUIGameState(result.game_data)
                }
            });
	});
    if (penalize_me){
        $("#discardCardModal").modal('show')
    }
    var updateUIGameState = function(game_data){
        var players = game_data.players
        var is_my_turn = false
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
            if (i == game_data.turn && players[i].user_name == user_name){
                is_my_turn = true
            }
            $('#coins'+i).text(players[i].n_coins)
            for (var j = 0; j < 2; j++){
               if (j >= players[i].cards.length){
                   $('#mycard'+j).empty()
               }else{
                   $('#mycard'+j).text(players[i].cards[j].name)
               }
                       

            }
        }
        if(is_my_turn){
            $('.turn_button').removeAttr('disabled')
        }else{
            $('.turn_button').attr('disabled', 'disabled')
        }
        var activity_log = game_data.activity_log
        $("#act_list").empty()
        for (var i = activity_log.length - 1; i >= 0; i--){
            if (i == activity_log.length -1){
                $('#latest_activity').text(activity_log[i])
            }else{
                $('#act_list').append('<li class="list-group-item">'+activity_log[i]+'</li>')
            }
        }
        if("penalize" in game_data && game_data.penalize == user_name){
            $("#discardCardModal").modal('show')
        }
    }
});
