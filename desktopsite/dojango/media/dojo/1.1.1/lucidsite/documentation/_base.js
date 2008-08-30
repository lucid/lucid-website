dojo.provide("lucidsite.documentation._base");
dojo.require("dojox.highlight");
dojo.require("dojox.highlight.languages._www");
dojo.require("dojox.highlight.languages.pygments._www");

var initCode = function(){
	dojo.query("code").forEach(dojox.highlight.init);
};	
dojo.addOnLoad(initCode); 