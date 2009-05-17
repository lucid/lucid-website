dojo.provide("lucidsite.lucidsite");
dojo.require("dojo.string");
dojo.require("dojox.analytics.Urchin");
dojo.require("dijit._base");
dojo.require("dijit.TooltipDialog");
dojo.require("dijit.form.Button");
dojo.require("dijit.form.TextBox");

lucidsite = {
    closeMsg: function(node){
        node = dojo.byId(node);
        if(!node) return;
        dojo.fadeOut({
            duration: 500,
            node: node,
            onEnd: function(){
                dojo.animateProperty({
                    node: node,
                    properties: {
                        height: {end: 0}
                    }
                }).play();
            }
        }).play();
    },
    sbox: function(node, e){
        node = dojo.byId(node);
        var str = "Search";
        if(node.value == "" && e == "blur"){
            node.value = str;
        }
        else if(node.value == str && e == "focus"){
            node.value = "";
        }
    },
    loginPopup: function(e){
        dojo.stopEvent(e);
        var node = e.target;
        var widget = dijit.byId("loginPopup");
        dijit.popup.open({
            popup: widget,
            around: node,
            orient: "TR"
        });
        var c = dojo.connect(widget, "onBlur", this, function(){
            dojo.disconnect(c);
            dijit.popup.close(widget);
        });
    }
};

dojo.addOnLoad(function() {
    var tracker = new dojox.analytics.Urchin({ 
		acct:"UA-5887536-1"
	});
});
