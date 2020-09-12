if(Cookies.get('preloaded') !== '1'){
		$(window).on('load', function() {
		setTimeout(function() {
			$("#loader-wrapper").fadeOut();
		}, 1000);
		});
	}
	else{
		$("#loader-wrapper").css('display','none');
	}
	Cookies.set('preloaded', 1);