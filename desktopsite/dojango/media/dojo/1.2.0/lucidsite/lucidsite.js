dojo.provide("lucidsite.lucidsite");
dojo.require("dojox.analytics.Urchin");
dojo.require("dijit._base");

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
    }
};

dojo.addOnLoad(function() {
    var tracker = new dojox.analytics.Urchin({ 
		acct:"UA-5887536-1"
	});
});
