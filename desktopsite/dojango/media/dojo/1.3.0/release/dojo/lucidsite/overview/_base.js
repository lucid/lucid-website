/*
	Copyright (c) 2004-2009, The Dojo Foundation All Rights Reserved.
	Available via Academic Free License >= 2.1 OR the modified BSD license.
	see: http://dojotoolkit.org/license for details
*/


if(!dojo._hasResource["lucidsite.overview._base"]){ //_hasResource checks added by build. Do not use _hasResource directly in your code.
dojo._hasResource["lucidsite.overview._base"] = true;
dojo.provide("lucidsite.overview._base");
dojo.require("dojox.image.SlideShow");
dojo.require("dojo.data.ItemFileReadStore");

dojo.addOnLoad(function() {
	var req = {
		query: {
			imageUrl: "*"
		}
	}
	dijit.byId("gallery").setDataStore(galleryStore, req);
});

}
