dojo.provide("lucidsite.index");
dojo.require("dijit.layout.TabContainer");
dojo.require("dijit.layout.ContentPane");
dojo.require("dojox.widget.Dialog");
dojo.require("dojox.av.FLVideo");
dojo.require("dojox.av.widget.Player");
dojo.require("dojox.av.widget.PlayButton");
dojo.require("dojox.av.widget.VolumeButton");
dojo.require("dojox.av.widget.ProgressSlider");
dojo.require("dojox.av.widget.Status");

dojo.addOnLoad(function(){
    dojo.query(".PlayerScreen", "intro-video-player").style({width: "896px", height: "504px"});
    dojo.connect(dijit.byId("intro-video-dialog"), "show", function(){
        setTimeout(dojo.hitch(dijit.byId("intro-video-player").children[0], "onClick"), 2000);
    });
    dojo.connect(dijit.byId("intro-video-dialog"), "hide", function(){
        var v = dijit.byId("intro-video-player");
        if(v.media.isPlaying) v.children[0].onClick();
    });
    setTimeout(function(){
        dojo.place("intro-video-player", "intro-video-dialog", "first");
    }, 200);
});

