dojo.provide("lucidsite.repository.Rating");
dojo.require("dojox.widget.Rating");

dojo.declare("lucidsite.repository.Rating", dojox.widget.Rating, {
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
