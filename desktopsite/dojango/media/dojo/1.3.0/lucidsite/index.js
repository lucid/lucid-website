dojo.provide("lucidsite.index");
dojo.require("dijit.layout.TabContainer");
dojo.require("dijit.layout.ContentPane");
dojo.require("dojox.av.FLVideo");
dojo.require("dojox.av.widget.Player");
dojo.require("dojox.av.widget.PlayButton");
dojo.require("dojox.av.widget.VolumeButton");
dojo.require("dojox.av.widget.ProgressSlider");
dojo.require("dojox.av.widget.Status");
dojo.require("dojox.fx.scroll");
dojo.require("dojox.fx.easing");

lucidsite.showVideo = function(){
    var nl = dojo.query("#intro .video").addClass("shown");
    setTimeout(dojo.hitch(dijit.byId("intro-video-player").children[0], "onClick"), 1500);
    dojox.fx.smoothScroll({
        node: "intro-video-player",
        win: window,
        easing: dojox.fx.easing.bounceOut,
        duration: 800
    }).play();
}

lucidsite.hideVideo = function(){
    var v = dijit.byId("intro-video-player");
    dojox.fx.smoothScroll({
        node: document.body,
        win: window,
        easing: dojox.fx.easing.bounceOut,
        duration: 800,
        onEnd: function(){
            v.media.pause();
        }
    }).play();
    setTimeout(function(){
        dojo.query("#intro .video").removeClass("shown");
        if(v.media.isPlaying) v.children[0].onClick();
    }, 200);
}

dojo.addOnLoad(function(){
    dojo.query(".PlayerScreen", "intro-video-player").style({width: "888px", height: "499px"});
});
