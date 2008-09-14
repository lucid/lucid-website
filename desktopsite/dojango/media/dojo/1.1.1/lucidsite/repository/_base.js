dojo.provide("lucidsite.repository._base");
dojo.require("lucidsite.repository.Rating");
dojo.require("dijit.layout.TabContainer");
dojo.require("dijit.layout.ContentPane");
dojo.require("dojox.fx");

dojo.mixin(lucidsite.repository, {
	toggle: function(node) {
		node = dojo.byId(node);
		if(dojo.style(node, "display") == "none") {
			dojo.style(node, {
				display: "block",
				height: "auto"
			});
			var anim = dojox.fx.wipeTo({
				node: node,
				height: node.clientHeight
			});
			dojo.style(node, "height", "0px");
			setTimeout(dojo.hitch(anim, "play"), 75);
		}
		else {
			dojox.fx.wipeTo({
				node: node,
				height: 0,
				onEnd: function() {
					setTimeout(function() {
						dojo.style(node, "display", "none");
					}, 75);
				}
			}).play();
		}
	}
})
