dojo.provide("lucidsite.documentation._base");
dojo.require("dojox.highlight");
dojo.require("dojox.highlight.languages._www");
dojo.require("dojox.highlight.languages.pygments._www");

var initCode = function(){
	dojo.query("code").forEach(function(node) {
	    node.innerHTML = node.innerHTML.replace(/\</gi,"&lt;").replace(/\</gi,"&gt;").replace(/\&/gi,"&amp;")
	    dojox.highlight.init(node);
	});
};	
dojo.addOnLoad(initCode); 
