dojo.provide("lucidsite.forum");
dojo.require("dojox.data.QueryReadStore");
dojo.require("dijit.form.FilteringSelect");

lucidsite.forum = {
	toggle: function(id, type) {
		if(dojo.style(id, "display") == "none")
			dojo.style(id, "display", type || "block");
		else
			dojo.style(id, "display", "none");
	},
	togglePost: function(id) {
		this.toggle('snap_post_sum'+id, 'inline');
		this.toggle('snap_post_view'+id);
	},
	toggleEdit: function(id) {
		//this.toggle('post_text'+id);
		this.toggle('snap_post_text'+id);
		this.toggle('snap_post_edit'+id)
	},
	preview: function(form_id) {
		var previewDiv = dojo.byId("snap_preview_addpost");
		var form = dojo.byId(form_id);
		dojo.xhrPost({
			url: SNAP_PREFIX + '/rpc/preview/',
			content: {
				text: form.post.value
			},
			load: function(data) {
				previewDiv.innerHTML = data.preview
				dojo.style(previewDiv, "display", "block");
                dojo.style(previewDiv.parentNode, "display", "block");
			},
			error: function(err) {
		        var errordiv = document.getElementById("thread_rpc_feedback");
				previewDiv.innerHTML = "There was an error previewing your post.";
				dojo.style(previewDiv, "display", "block");
			},
			handleAs: "json"
		})
	},
	revision: function(orig_id, show_id) {
		var div_text = dojo.byId('snap_post_text' + orig_id)
	    var div_links = dojo.byId('post_revision_links' + orig_id)
		dojo.xhrGet({
			url: SNAP_PREFIX + "/rpc/postrev/",
			content: {
				orig: orig_id,
				show: show_id
			},
			load: function(data) {
				div_text.innerHTML = data.text;
				var html = ""
				if(data.prev_id !== '') {
	                //links_html += '<a href="#" onClick="revision(\''
					html += '<a href="javascript://" onClick="lucidsite.forum.revision(\''
	                + orig_id + '\',\'' + data.prev_id
	                + '\');">&#171; previous</a>';
				}
				html += ' <b style="color: #c00;">This message has been revised</b> '
				if(data.rev_id !== '') {
	                //html += '<a href="#" onClick="revision(\''
                	html += '<a href="javascript://" onClick="lucidsite.forum.revision(\''
	                + orig_id + '\',\'' + data.rev_id
	                + '\');">next &#187;</a>';
	            }
	            div_links.innerHTML = html;
			},
			handleAs: "json"
		})
	},
	toggleVariable: function(action, oclass, oid, msgdivid) {
	    // This function sends an RPC request to the server to toggle a
	    // variable (usually a boolean).  The server response with text
	    // to replace the button clicked and a status message.
		
		var div = dojo.byId(action + oid);
		
		dojo.xhrPost({
			url: SNAP_PREFIX + '/rpc/action/',
			content: {
				action: action,
				oclass: oclass,
				oid: oid
			},
			load: function(data) {
				div.innerHTML = data.link;
				dojo.byId(msgdivid).innerHTML = '<p class="rpc_message">' + data.msg + "</p>";
			},
			error: function(err) {
				div.innerHTML = "<b>ERROR</b>"
			},
			handleAs: "json"
		})
		
	},
	addAutoComplete: function(store, node) {
		var auto = new dijit.form.FilteringSelect({
			hasDownArrow: false,
			store: store,
			pageSize: 10
		})
		var div = dojo.doc.createElement("div");
		div.appendChild(auto.domNode);
		var closeButton = dojo.doc.createElement("button");
		closeButton.innerHTML = "x";
		dojo.connect(closeButton, "onclick", this, function() {
			div.parentNode.removeChild(div);
			auto.destroy();
		})
		div.appendChild(closeButton);
		dojo.byId(node).appendChild(div)
	},
	compileList: function(node, targetId) {
		var values = [];
		dojo.query(".dijitTextBox", node).forEach(function(wid) {
			try {
				wid = dijit.byNode(wid);
			} 
			catch(e) {
				return;
			}
			var value = wid.getDisplayedValue();
			if(value && wid.isValid())
				values.push(value);
		})
		dojo.byId(targetId).value = values.join(",")
	},
    quotePost: function(id){
        var tarea = dojo.query("#add_post_div textarea")[0];
        var text = dojo.byId("snap_post_text_quote"+id)[dojo.isIE ? "innerText" : "textContent"].split("\n");
        var newtext = "";
        for(var i=0;i<text.length;i++){
            if(text[i].replace(" ", "") == "")
                newtext += "> \n";
            else
                newtext += "> "+text[i]+"\n";
        }
        if(tarea.value == "")
            tarea.value = newtext;
        else
            tarea.value += "\n"+newtext;
        tarea.focus();
    }
}

dojo.forEach([
	"Csticky",
	"Gsticky",
	"Watch",
	"Close"
], function(method) {
	lucidsite.forum["set"+method] = function(id) {
		this.toggleVariable(method.toLowerCase(), 'thread', id, 'thread_rpc_feedback');
	}
})

dojo.forEach([
	"Censor",
	"Abuse"
], function(method) {
	lucidsite.forum["set"+method] = function(id) {
		this.toggleVariable(method.toLowerCase(), 'post', id, 'post_rpc_feedback' + id);
	}
})
