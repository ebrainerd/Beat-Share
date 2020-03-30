var audio;

//Hide Pause Initially
$(document).ready(function () {
    $('#pause').hide();
});

function loadSong(url, title, username){

    if ( audio != null ) {
        audio.pause();
        audio.src = url;
    }
    else {
        audio = new Audio( url );
    }

    audio.load();
    audio.play();

    $('#play').hide();
    $('#stop').show();
    $('#pause').show();
    showDuration();


	if(!audio.currentTime){
		$('#duration').html('0.00');
	}

	$('#audio-player .title').text( title );
    $('#audio-player .artist').text( username );

	//Insert Cover Image
//	$('img.cover').attr('src', "{{ STATIC_URL }} static/main/css_images/artwork-default.png");
}

//Play Button
$(document).ready(function () {
    $('#play').click(function() {
        audio.play();
        $('#play').hide();
        $('#pause').show();
        $('#duration').fadeIn(400);
        showDuration();
    });
});

//Pause Button
$('#pause').click(function(){
	audio.pause();
	$('#pause').hide();
	$('#play').show();
});

//Stop Button
$('#stop').click(function(){
	audio.pause();
	audio.currentTime = 0;
	$('#pause').hide();
	$('#play').show();
	$('#duration').fadeOut(400);
});

//Volume Control
$('#volume').change(function(){
	audio.volume = parseFloat(this.value / 10);
});

//Time Duration
function showDuration(){
	$(audio).bind('timeupdate', function(){
		//Get hours and minutes
		var s = parseInt(audio.currentTime % 60);
		var m = parseInt((audio.currentTime / 60) % 60);
		//Add 0 if seconds less than 10
		if (s < 10) {
			s = '0' + s;
		}
		$('#duration').html(m + '.' + s);
		var value = 0;
		if (audio.currentTime > 0) {
			value = Math.floor((100 / audio.duration) * audio.currentTime);
		}
		$('#progress').css('width',value+'%');
	});
}
