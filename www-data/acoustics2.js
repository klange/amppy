var volume;
var stateTimer;
var templates = {};
var jsonSource = 'json.pl';
var playingTimer;
var elapsedTime = 0;
var totalTime = 0;

$(document).ready(function() {
	$("#queue-list").sortable({
		placeholder: "queue-song-placeholder",
		axis: "y",
		handle: ".queue-song-handle"
	});

	// templating
	templates.queueSong = $("li.queue-song").first().clone();
	templates.nowPlayingPanel = $("#now-playing-panel").clone();

	playerStateRequest();
	if (stateTimer) clearInterval(stateTimer);
	stateTimer = setInterval(function() {playerStateRequest();}, 15000)
});

function readableTime(length) {
	if (length < 0) {length = 0;}
	var seconds = length % 60;
	var minutes = Math.floor(length / 60) % 60;
	var hours = Math.floor(length / 3600);
	if (hours) {
		return sprintf("%d:%02d:%02d",hours,minutes,seconds);
	} else {
		return sprintf("%d:%02d",minutes,seconds);
	}
}

function startPlayingTimer() {
	if (playingTimer) clearInterval(playingTimer);
	playingTimer = setInterval(function() { updatePlayingTime() }, 1000);
}

function updatePlayingTime() {
	if(elapsedTime < totalTime) {
		$('#now-playing-time').html(readableTime(++elapsedTime));
		$('#now-playing-progress').progressbar({value: Math.floor(100 * (elapsedTime/totalTime))});
	}
}

function playerStateRequest() {
	$.getJSON(
		jsonSource,
		function (json) {handlePlayerStateRequest(json);}
	);
}

function handlePlayerStateRequest(json) {
	// volume
	if (json.player && json.player.volume != undefined) {
		volume = parseInt(json.player.volume);
		$("#controls-volume").html((volume / 10) + 1);
	} else {
		$("#controls-volume").html("-");
	}

	// user
	if (json.who) {
		$("#header-bar-user-message").html("logged in as");
		$("#user-name").html(json.who);
	}

	// now playing
	var nowPlaying = json.now_playing;
	var nowPlayingPanel = templates.nowPlayingPanel.clone();
	$("#now-playing-panel").empty();
	if (nowPlaying) {
		$("#now-playing-title", nowPlayingPanel).html(nowPlaying.title);
		$("#now-playing-album", nowPlayingPanel).html(nowPlaying.album);
		$("#now-playing-artist", nowPlayingPanel).html(nowPlaying.artist);
		$("#now-playing-total", nowPlayingPanel).html(readableTime(nowPlaying.length));
		totalTime = nowPlaying.length;
		startPlayingTimer();
		elapsedTime = Math.round(((new Date().getTime())/1000)) - json.player.song_start;
		$("#now-playing-time", nowPlayingPanel).html(readableTime(elapsedTime));
		$("#nothing-playing-info", nowPlayingPanel).remove();
		$("#now-playing-panel").replaceWith(nowPlayingPanel);
		$("#now-playing-album-art-img").reflect({height: 16});
		$("#now-playing-progress").progressbar({value: Math.floor(100 * (elapsedTime/totalTime))});
	} else {
		$("#now-playing-album-art", nowPlayingPanel).remove();
		$("#now-playing-info", nowPlayingPanel).remove();
		$("#now-playing-panel").replaceWith(nowPlayingPanel);
		totalTime = -1;
	}

	// the queue
	$("#queue-list").empty();
	var total_length = 0;
	for (var i in json.playlist) {
		var song = json.playlist[i];
		var entry = templates.queueSong.clone();
		$(".queue-song-title", entry).html(song.title);
		$(".queue-song-artist", entry).html(song.artist);
		var minutes = '' + Math.floor(song.length / 60);
		var seconds = '' + song.length % 60;
		while (seconds.length < 2) {
			seconds = "0" + seconds;
		}
		$(".queue-song-time", entry).html(minutes + ":" + seconds);
		total_length += song.length;
		entry.appendTo("#queue-list");
	}
	var length = $("#queue-list").contents().length;
	if (length == 1) {
		$("#queue-song-count").html("One song");
	} else {
		$("#queue-song-count").html(length + " songs");
	}
	$("#queue-length").html(readableTime(total_length));
}

function controlPlayPause() {
	$.getJSON(
			jsonSource + '?mode=start',
		function (data) {handlePlayerStateRequest(data);}
	);
}

function controlStop() {
	$.getJSON(
		jsonSource + '?mode=stop',
		function (data) {handlePlayerStateRequest(data);}
	);
}

function controlNext() {
	$.getJSON(
		jsonSource + '?mode=skip',
		function (data) {handlePlayerStateRequest(data);}
	);
}

function controlVolumeDown() {
	if (volume != undefined) {
		volume -= 10;
		$.getJSON(
			jsonSource + '?mode=volume;value=' + volume,
			function (data) {handlePlayerStateRequest(data);}
		);
	}
}

function controlVolumeUp() {
	if (volume != undefined) {
		volume += 10;
		$.getJSON(
			jsonSource + '?mode=volume;value=' + volume,
			function (data) {handlePlayerStateRequest(data);}
		);
	}
}

$("#messageBox").ready(function() {
	$("#messageBox").dialog({
		autoOpen: false,
		modal: true,
		buttons: {"ok": function() {
			$(this).dialog("close");
			// set the text back to default
			// (so we know if someone forgot to set it in another call)
			$(this).html("no text... why?");
		}}
	});

	$("#messageBox").ajaxError(function (e, xhr, opts, err) {
		$(this).dialog('option', 'title', 'Communication Error');
		$(this).html(xhr.responseText);
		$(this).dialog('open');
	});
});

