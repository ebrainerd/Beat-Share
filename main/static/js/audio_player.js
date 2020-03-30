function loadSong(url){
    var player = document.getElementById('player');

    player.src = url;

    player.load();
    player.play();
}
