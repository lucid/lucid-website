dojo.provide("repository.Rating");
dojo.require("dojox.widget.Rating");

dojo.declare("repository.Rating", dojox.widget.Rating, {
	noInput: false,
	_rendered: false,
	_renderStars: function() {
		if(this._rendered && this.noInput) return;
		this._rendered = true;
		this.inherited(arguments);
	}
})
