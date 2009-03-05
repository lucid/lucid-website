dojo.provide("lucidsite.blog");

//hide honeypot field
dojo.addOnLoad(function() {
	dojo.query("#comment_form_table tr:last-child").style("display", "none");
});