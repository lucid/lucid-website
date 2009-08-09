/*
	Copyright (c) 2004-2009, The Dojo Foundation All Rights Reserved.
	Available via Academic Free License >= 2.1 OR the modified BSD license.
	see: http://dojotoolkit.org/license for details
*/


if(!dojo._hasResource["lucidsite.documentation._base"]){ //_hasResource checks added by build. Do not use _hasResource directly in your code.
dojo._hasResource["lucidsite.documentation._base"] = true;
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

}
