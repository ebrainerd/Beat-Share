function loadSong(url){
    var player = document.getElementById('player');
    var sourceMp3 = document.getElementById('player');

    sourceMp3.src = url;

    player.load();
    player.play();
}
