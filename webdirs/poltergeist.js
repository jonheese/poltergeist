function file_exists(sitename, x) {
	var loc = window.location;
	var url = loc.protocol + "//" + loc.host + "/static/" + sitename + "/" + sitename + x + ".mp3";
	var http = new XMLHttpRequest();
	http.open('HEAD', url, false);
	http.send();
	return http.status != 404;
}

function set_mp3_source(sitename) {
	baseurl = "/static/" + sitename;
	if (file_exists(sitename, "")) {
		document.getElementById("player").src = baseurl + "/" + sitename + ".mp3";
	}
	else {
		max = 1;
		for (i = 1; i < 30; i++) {
			if (!file_exists(sitename, i)) {
				break;
			}
			max = i;
		}
		var x = Math.floor((Math.random() * max) + 1);
		document.getElementById("player").src = baseurl + "/" + sitename + x + ".mp3";
	}
}
