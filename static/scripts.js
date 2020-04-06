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
});
