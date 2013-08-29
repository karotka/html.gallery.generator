var Karotka = {};
/* MAKRA */

/* getElementById */
Karotka.gEl = function(ids){
	return document.getElementById(ids);
};

/* vytvarim HTML uzel */
Karotka.cEl = function(name){
	return document.createElement(name);
};

/* novy element do body */
Karotka.bodyAddEl = function( el ) {
	document.getElementsByTagName("body")[0].appendChild(el);
};

/* vracim rozmery documentu */
Karotka.getDocSize = function(){
	var x	= document.documentElement.clientWidth && (Karotka.browser.klient != 'op') ? document.documentElement.clientWidth : document.body.clientWidth;
	var y	= document.documentElement.clientHeight && (Karotka.browser.klient != 'op') ? document.documentElement.clientHeight : document.body.clientHeight;
	if ((Karotka.browser.klient == 'saf') || (Karotka.browser.klient == 'kon')){
		y = window.innerHeight;
	}
	return {width:x,height:y};
};

/**
 * vracim polohu "obj" ve strance nebo uvnitr objektu ktery predam jako treti
 * argument, argument dir urcuje zda jde o vertikalni (left), nebo
 * horizontalni pozici (top)
 */
Karotka.getBoxPosition = function(obj, dir) {
	if(arguments[2]){
		return Karotka._getInBoxPosition(obj, dir, arguments[2])
	} else {
		return Karotka._getBoxPosition(obj, dir)
	}
};

/* vraci pozici uvnitr objektu refBox */
Karotka._getInBoxPosition = function(obj, dir, refBox) {
	var pos = 0;
	do {
		pos = (dir == 'top') ? pos + obj.offsetTop : pos + obj.offsetLeft;
		obj = obj.offsetParent;
	} while (obj.offsetParent != refBox);
	return pos;
};

/* vraci pozici ve strance */
Karotka._getBoxPosition = function(obj, dir)    {
	var pos = 0;
	while (obj.offsetParent) {
		pos = (dir == 'top') ? pos + obj.offsetTop : pos + obj.offsetLeft;
		obj = obj.offsetParent;
	}
	return pos;
};

/* vraci odscrollovani stranky */
Karotka.getScrollPos = function() {
	if (document.documentElement.scrollTop || document.documentElement.scrollLeft) {
		var ox = document.documentElement.scrollLeft;
		var oy = document.documentElement.scrollTop;
	} else if (document.body.scrollTop) {
		var ox = document.body.scrollLeft;
		var oy = document.body.scrollTop;
	} else {
		var ox = 0;
		var oy = 0;
	}
 	return {x:ox, y:oy};
};

Karotka.getElementsByClass = function(searchClass, tag, node) {
	var classElements = new Array();
	if (node == null) {
		node = document;
    }
	if (tag == null) {
		tag = '*';
    }
	var els = node.getElementsByTagName(tag);

	var elsLen = els.length;
	var pattern = new RegExp("(^|\\\\s)" + searchClass + "(\\\\s|$)");
	for (i = 0, j = 0; i < elsLen; i++) {
		if (pattern.test(els[i].className)) {
			classElements[j] = els[i];
			j++;
		}
	}
	return classElements;
}

Karotka.addEventPictures = function() {
    var elements  = Karotka.getElementsByClass("picture", "a");
    window.pictures = new Array(elements.length);
    for (var i = 0; i < elements.length; i++) {
        window.pictures[i] = elements[i];
        elements[i].onclick = PhotoPopUp.show;
    }
}

Karotka.basename = function(string) {
    var arr = string.toString().split("/");
    return arr[arr.length - 1];
}


PhotoPopUp = {

    // true, if popUp is visible
    showPopUp : false,

    //
    timeout   : 2000,

    //
    runPlay   : false,

    //
    elId      : null,
    elIdTop   : null,
    img       : null,
    url       : "",

    show : function() {

        if (PhotoPopUp.checkVisible()) {

            PhotoPopUp.hide();
            //PhotoPopUp.show();
            return false;
        }


        var trgTop = 5 + Karotka.getScrollPos().y;
        var trgLeft = 10;
        var topPosRep = (document.attachEvent && !window.opera) ? 2 : 0;

        if (PhotoPopUp.url == "") {
            //alert(PhotoPopUp.url);
            PhotoPopUp.url = this;
        }
        //alert(PhotoPopUp.url);
        PhotoPopUp.render(PhotoPopUp.url);

        PhotoPopUp.elId      = "photoPopUp";
        PhotoPopUp.showPopUp = true;

        Karotka.gEl('photoPopUp').style.top = trgTop + 'px';
        Karotka.gEl('photoPopUp').style.left = trgLeft + 'px';

        return false;
    },

    hide : function() {
        el = Karotka.gEl(PhotoPopUp.elId);
        el.parentNode.removeChild(el);
        el = null;
        PhotoPopUp.showPopUp = false;

        InfoPopUp.hide()
        PhotoPopUp.url = "";

        return false;
    },

    checkVisible : function() {
        return PhotoPopUp.showPopUp;
    },

    play : function() {
        PhotoPopUp.runPlay = true;
        Karotka.gEl("play").src = window.STATIC + "/run_play.gif";
        setTimeout("PhotoPopUp.next(true)", PhotoPopUp.timeout);
    },

    stop : function() {
        PhotoPopUp.runPlay = false;
        Karotka.gEl("play").src = window.STATIC + "/play.gif";
    },

    render : function(url) {
        el           = Karotka.cEl("div");
        el.className = "photoPopUp";
        el.id        = "photoPopUp";

        PhotoPopUp.img = Karotka.cEl("img");
        PhotoPopUp.img.src = url;
        //PhotoPopUp.img.onclick = PhotoPopUp.hide;
        PhotoPopUp.img.onclick = PhotoPopUp.next;

        var div = Karotka.cEl("div");
        div.innerHTML  = "<img src=\"" + window.STATIC + '/close.gif" id="close" onclick="return PhotoPopUp.hide()">';
        div.innerHTML += "<img src=\"" + window.STATIC + '/info.gif" id="info" onclick="return InfoPopUp.show()">';
        div.innerHTML += "<img src=\"" + window.STATIC + '/stop.gif" id="stop" onclick="return PhotoPopUp.stop()">';
        div.innerHTML += "<img src=\"" + window.STATIC + '/next.gif" id="next" onclick="return PhotoPopUp.next()">';
        div.innerHTML += "<img src=\"" + window.STATIC + '/prev.gif" id="prev" onclick="return PhotoPopUp.prev()">';
        div.innerHTML += "<img src=\"" + window.STATIC + '/play.gif" id="play" onclick="return PhotoPopUp.play()">';
        if (url.title) {
            //div.innerHTML += '<span id="title">'+ url.title +'</span>';
        }

        d = el.appendChild(div);
        d.appendChild(PhotoPopUp.img);

        Karotka.bodyAddEl(el)

        PhotoPopUp.addInfo(url)
    },

    addInfo : function(url) {
        url = Karotka.basename(url);

        if (!window.photos) {
            Karotka.gEl("info").style.display = "none";
            return;
        }
        var match = false;
        for (var i = 0; i < window.photos.length; i++) {
            if (window.photos[i].url == url) {
                match = true;
            }
        }
        if (!match) {
            Karotka.gEl("info").style.display = "none";
        } else {
            Karotka.gEl("info").style.display = "block";
        }
    },

    prev : function() {

        InfoPopUp.hide();

        for (var i = 0; i < window.pictures.length; i++) {
            if (window.pictures[i] == PhotoPopUp.img.src) {
                if (i == 0) {
                    PhotoPopUp.img.src = window.pictures[window.pictures.length - 1];
                    break;
                }
                PhotoPopUp.img.src = window.pictures[i-1];
                break;
            }
        }
        PhotoPopUp.addInfo(PhotoPopUp.img.src);
        return false;
    },

    hidePrev : function() {
        if (PhotoPopUp.img.src == window.pictures[0]) {
            Karotka.gEl("prev").style.display = "none";
        }
        Karotka.gEl("next").style.display = "block";
    },

    next : function(play) {

        InfoPopUp.hide();

        for (var i = 0; i < window.pictures.length; i++) {
            if (window.pictures[i] == PhotoPopUp.img.src) {
                if (i + 1 == window.pictures.length) {
                    PhotoPopUp.img.src = window.pictures[0];
                    break;
                }
                PhotoPopUp.img.src = window.pictures[i+1];
                break;
            }
        }
        PhotoPopUp.addInfo(PhotoPopUp.img.src);

        if (PhotoPopUp.runPlay && play) {
            PhotoPopUp.play();
        }

        return false;
    },

    hideNext : function(status) {
        if (window.pictures[window.pictures.length - 1] == PhotoPopUp.img.src) {
            Karotka.gEl("next").style.display = "none";
        }
        if (!status)
            Karotka.gEl("prev").style.display = "block";
    }
}

InfoPopUp = {

    // true, if popUp is visible
    showPopUp : false,
    elId      : null,

    show : function() {

        if (InfoPopUp.checkVisible()) {
            InfoPopUp.hide();
            return false;
        }

        elCorect = Karotka.gEl("photoPopUp");
        y = Karotka.getBoxPosition(elCorect, 'top');
        x = Karotka.getBoxPosition(elCorect, 'left');

        var trgTop  = 15 + y;
        var trgLeft = 15 + x;
        var topPosRep = (document.attachEvent && !window.opera) ? 2 : 0;

        InfoPopUp.render();

        InfoPopUp.elId      = "infoPopUp";
        InfoPopUp.showPopUp = true;

        Karotka.gEl('infoPopUp').style.top = trgTop + 'px';
        Karotka.gEl('infoPopUp').style.left = trgLeft + 'px';

        return false;
    },

    hide : function() {
        el = Karotka.gEl(InfoPopUp.elId);
        if (el) {
            el.parentNode.removeChild(el);
            el = null;
            InfoPopUp.showPopUp = false;
        }
        return false;
    },

    checkVisible : function() {
        return InfoPopUp.showPopUp;
    },

    getInfo : function() {
        var url = Karotka.basename(PhotoPopUp.img.src);
        var match = false;
        for (var i = 0; i < window.photos.length; i++) {
            if (window.photos[i].url == url) {
                return window.photos[i].exif;
            }
        }
        return "";
    },

    render : function() {
        el           = Karotka.cEl("div");
        el.className = "infoPopUp";
        el.id        = "infoPopUp";
        el.onclick   = InfoPopUp.hide;

        var div = Karotka.cEl("div");
        div.innerHTML  = InfoPopUp.getInfo();

        el.appendChild(div);

        Karotka.bodyAddEl(el)
    }
}
