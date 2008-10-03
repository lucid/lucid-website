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
