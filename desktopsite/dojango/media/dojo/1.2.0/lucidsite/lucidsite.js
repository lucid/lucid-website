dojo.provide("lucidsite.lucidsite");
dojo.require("dojox.analytics.Urchin");

dojo.addOnLoad(function() {
    var tracker = new dojox.analytics.Urchin({ 
		acct:"UA-5887536-1"
	});
});
