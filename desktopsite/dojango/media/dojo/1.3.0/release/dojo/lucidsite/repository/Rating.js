/*
	Copyright (c) 2004-2009, The Dojo Foundation All Rights Reserved.
	Available via Academic Free License >= 2.1 OR the modified BSD license.
	see: http://dojotoolkit.org/license for details
*/


if(!dojo._hasResource["lucidsite.repository.Rating"]){ //_hasResource checks added by build. Do not use _hasResource directly in your code.
dojo._hasResource["lucidsite.repository.Rating"] = true;
dojo.provide("lucidsite.repository.Rating");
dojo.require("dojox.form.Rating");

dojo.declare("lucidsite.repository.Rating", dojox.form.Rating, {
	noInput: false,
	_rendered: false,
	canVote: false,
	notifyNode: "",
	notifyText: "Thanks for voting!",
	clearText: "Vote cleared!",
	loginText: "Log in first",
	versionId: 0,
	_renderStars: function() {
		if(this._rendered && this.noInput) return;
		this._rendered = true;
		this.inherited(arguments);
	},
	onChange: function(value) {
		if(this.noInput) return;
		if(!this.canVote) {
			this.noInput = true;
			this.setValue(0);
			this.noInput = false;
			this.onRatingSave(-1);
			return;
		}
		//tell the server
		dojo.xhrPost({
			url: "/repository/vote/",
			content: {
				versionId: this.versionId,
				value: value
			},
			error: function() {
				alert("There was a problem submitting your vote.\nPlease try again.")
			}
		})
		//send notification
		this.onRatingSave(value);
	},
	onRatingSave: function(value) {
		if(!this.notifyNode) return;
		n = dojo.byId(this.notifyNode);
		dojo.style(n, "opacity", 0);
		dojo.fadeIn({node: n}).play();
		n.innerHTML = (value < 0 ? this.loginText : (value ? this.notifyText : this.clearText));
	}
})

}
