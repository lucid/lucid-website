/*
	Copyright (c) 2004-2009, The Dojo Foundation All Rights Reserved.
	Available via Academic Free License >= 2.1 OR the modified BSD license.
	see: http://dojotoolkit.org/license for details
*/

/*
	This is a compiled version of Dojo, built for deployment and not for
	development. To get an editable version, please visit:

		http://dojotoolkit.org

	for documentation and information on getting the source.
*/

dojo.provide("lucidsite.documentation");
if(!dojo._hasResource["dojox.highlight._base"]){ //_hasResource checks added by build. Do not use _hasResource directly in your code.
dojo._hasResource["dojox.highlight._base"] = true;
dojo.provide("dojox.highlight._base");
/*=====
	dojox.highlight = {
		//	summary: 
		//		Syntax highlighting with language auto-detection package
		//
		//	description:
		//		
		//		Syntax highlighting with language auto-detection package.
		//		Released under CLA by the Dojo Toolkit, original BSD release 
		//		available from: http://softwaremaniacs.org/soft/highlight/
		//
		//		
	};
=====*/

;(function(){
	var dh = dojox.highlight,
		C_NUMBER_RE = '\\b(0x[A-Za-z0-9]+|\\d+(\\.\\d+)?)';
	
	// constants

	dh.constants = {
		IDENT_RE: '[a-zA-Z][a-zA-Z0-9_]*',
		UNDERSCORE_IDENT_RE: '[a-zA-Z_][a-zA-Z0-9_]*',
		NUMBER_RE: '\\b\\d+(\\.\\d+)?',
		C_NUMBER_RE: C_NUMBER_RE,
		// Common modes
		APOS_STRING_MODE: {
			className: 'string',
			begin: '\'', end: '\'',
			illegal: '\\n',
			contains: ['escape'],
			relevance: 0
		},
		QUOTE_STRING_MODE: {
			className: 'string',
			begin: '"', 
			end: '"',
			illegal: '\\n',
			contains: ['escape'],
			relevance: 0
		},
		BACKSLASH_ESCAPE: {
			className: 'escape',
			begin: '\\\\.', end: '^',
			relevance: 0
		},
		C_LINE_COMMENT_MODE: {
			className: 'comment',
			begin: '//', end: '$',
			relevance: 0
		},
		C_BLOCK_COMMENT_MODE: {
			className: 'comment',
			begin: '/\\*', end: '\\*/'
		},
		HASH_COMMENT_MODE: {
			className: 'comment',
			begin: '#', end: '$'
		},
		C_NUMBER_MODE: {
			className: 'number',
			begin: C_NUMBER_RE, end: '^',
			relevance: 0
		}
	};

	// utilities
	
	function esc(value){
		return value.replace(/&/gm, '&amp;').replace(/</gm, '&lt;').replace(/>/gm, '&gt;');
	}
	
	function verifyText(block){
		return dojo.every(block.childNodes, function(node){
			return node.nodeType == 3 || String(node.nodeName).toLowerCase() == 'br';
		});
	}

	function blockText(block){
		var result = [];
		dojo.forEach(block.childNodes, function(node){
			if(node.nodeType == 3){
				result.push(node.nodeValue);
			}else if(String(node.nodeName).toLowerCase() == 'br'){
				result.push("\n");
			}else{
				throw 'Complex markup';
			}
		});
		return result.join("");
	}

	function buildKeywordGroups(mode){
		if(!mode.keywordGroups){
			for(var key in mode.keywords){
				var kw = mode.keywords[key];
    			if(kw instanceof Object){  // dojo.isObject?
					mode.keywordGroups = mode.keywords;
				}else{ 
					mode.keywordGroups = {keyword: mode.keywords};
				}
				break;
			}
		}
	}
	
	function buildKeywords(lang){
		if(lang.defaultMode && lang.modes){
			buildKeywordGroups(lang.defaultMode);
			dojo.forEach(lang.modes, buildKeywordGroups);
		}
	}
	
	// main object

	var Highlighter = function(langName, textBlock){
		// initialize the state
		this.langName = langName;
		this.lang = dh.languages[langName];
		this.modes = [this.lang.defaultMode];
		this.relevance = 0;
		this.keywordCount = 0;
		this.result = [];
		
		// build resources lazily
		if(!this.lang.defaultMode.illegalRe){
			this.buildRes();
			buildKeywords(this.lang);
		}
		
		// run the algorithm
		try{
			this.highlight(textBlock);
			this.result = this.result.join("");
		}catch(e){
			if(e == 'Illegal'){
				this.relevance = 0;
				this.keywordCount = 0;
				this.partialResult = this.result.join("");
				this.result = esc(textBlock);
			}else{
				throw e;
			}
		}
	};

	dojo.extend(Highlighter, {
		buildRes: function(){
			dojo.forEach(this.lang.modes, function(mode){
				if(mode.begin){
					mode.beginRe = this.langRe('^' + mode.begin);
				}
				if(mode.end){
					mode.endRe = this.langRe('^' + mode.end);
				}
				if(mode.illegal){
					mode.illegalRe = this.langRe('^(?:' + mode.illegal + ')');
				}
			}, this);
			this.lang.defaultMode.illegalRe = this.langRe('^(?:' + this.lang.defaultMode.illegal + ')');
		},
		
		subMode: function(lexeme){
			var classes = this.modes[this.modes.length - 1].contains;
			if(classes){
				var modes = this.lang.modes;
				for(var i = 0; i < classes.length; ++i){
					var className = classes[i];
					for(var j = 0; j < modes.length; ++j){
						var mode = modes[j];
						if(mode.className == className && mode.beginRe.test(lexeme)){ return mode; }
					}
				}
			}
			return null;
		},

		endOfMode: function(lexeme){
			for(var i = this.modes.length - 1; i >= 0; --i){
				var mode = this.modes[i];
				if(mode.end && mode.endRe.test(lexeme)){ return this.modes.length - i; }
				if(!mode.endsWithParent){ break; }
			}
			return 0;
		},

		isIllegal: function(lexeme){
			var illegalRe = this.modes[this.modes.length - 1].illegalRe;
			return illegalRe && illegalRe.test(lexeme);
		},


		langRe: function(value, global){
			var mode =  'm' + (this.lang.case_insensitive ? 'i' : '') + (global ? 'g' : '');
			return new RegExp(value, mode);
		},
	
		buildTerminators: function(){
			var mode = this.modes[this.modes.length - 1],
				terminators = {};
			if(mode.contains){
				dojo.forEach(this.lang.modes, function(lmode){
					if(dojo.indexOf(mode.contains, lmode.className) >= 0){
						terminators[lmode.begin] = 1;
					}
				});
			}
			for(var i = this.modes.length - 1; i >= 0; --i){
				var m = this.modes[i];
				if(m.end){ terminators[m.end] = 1; }
				if(!m.endsWithParent){ break; }
			}
			if(mode.illegal){ terminators[mode.illegal] = 1; }
			var t = [];
			for(i in terminators){ t.push(i); }
			mode.terminatorsRe = this.langRe("(" + t.join("|") + ")");
		},

		eatModeChunk: function(value, index){
			var mode = this.modes[this.modes.length - 1];
			
			// create terminators lazily
			if(!mode.terminatorsRe){
				this.buildTerminators();
			}
	
			value = value.substr(index);
			var match = mode.terminatorsRe.exec(value);
			if(!match){
				return {
					buffer: value,
					lexeme: "",
					end:    true
				};
			}
			return {
				buffer: match.index ? value.substr(0, match.index) : "",
				lexeme: match[0],
				end:    false
			};
		},
	
		keywordMatch: function(mode, match){
			var matchStr = match[0];
			if(this.lang.case_insensitive){ matchStr = matchStr.toLowerCase(); }
			for(var className in mode.keywordGroups){
				if(matchStr in mode.keywordGroups[className]){ return className; }
			}
			return "";
		},
		
		buildLexemes: function(mode){
			var lexemes = {};
			dojo.forEach(mode.lexems, function(lexeme){
				lexemes[lexeme] = 1;
			});
			var t = [];
			for(var i in lexemes){ t.push(i); }
			mode.lexemsRe = this.langRe("(" + t.join("|") + ")", true);
		},
	
		processKeywords: function(buffer){
			var mode = this.modes[this.modes.length - 1];
			if(!mode.keywords || !mode.lexems){
				return esc(buffer);
			}
			
			// create lexemes lazily
			if(!mode.lexemsRe){
				this.buildLexemes(mode);
			}
			
			mode.lexemsRe.lastIndex = 0;
			var result = [], lastIndex = 0,
				match = mode.lexemsRe.exec(buffer);
			while(match){
				result.push(esc(buffer.substr(lastIndex, match.index - lastIndex)));
				var keywordM = this.keywordMatch(mode, match);
				if(keywordM){
					++this.keywordCount;
					result.push('<span class="'+ keywordM +'">' + esc(match[0]) + '</span>');
				}else{
					result.push(esc(match[0]));
				}
				lastIndex = mode.lexemsRe.lastIndex;
				match = mode.lexemsRe.exec(buffer);
			}
			result.push(esc(buffer.substr(lastIndex, buffer.length - lastIndex)));
			return result.join("");
		},
	
		processModeInfo: function(buffer, lexeme, end) {
			var mode = this.modes[this.modes.length - 1];
			if(end){
				this.result.push(this.processKeywords(mode.buffer + buffer));
				return;
			}
			if(this.isIllegal(lexeme)){ throw 'Illegal'; }
			var newMode = this.subMode(lexeme);
			if(newMode){
				mode.buffer += buffer;
				this.result.push(this.processKeywords(mode.buffer));
				if(newMode.excludeBegin){
					this.result.push(lexeme + '<span class="' + newMode.className + '">');
					newMode.buffer = '';
				}else{
					this.result.push('<span class="' + newMode.className + '">');
					newMode.buffer = lexeme;
				}
				this.modes.push(newMode);
				this.relevance += typeof newMode.relevance == "number" ? newMode.relevance : 1;
				return;
			}
			var endLevel = this.endOfMode(lexeme);
			if(endLevel){
				mode.buffer += buffer;
				if(mode.excludeEnd){
					this.result.push(this.processKeywords(mode.buffer) + '</span>' + lexeme);
				}else{
					this.result.push(this.processKeywords(mode.buffer + lexeme) + '</span>');
				}
				while(endLevel > 1){
					this.result.push('</span>');
					--endLevel;
					this.modes.pop();
				}
				this.modes.pop();
				this.modes[this.modes.length - 1].buffer = '';
				return;
			}
		},
	
		highlight: function(value){
			var index = 0;
			this.lang.defaultMode.buffer = '';
			do{
				var modeInfo = this.eatModeChunk(value, index);
				this.processModeInfo(modeInfo.buffer, modeInfo.lexeme, modeInfo.end);
				index += modeInfo.buffer.length + modeInfo.lexeme.length;
			}while(!modeInfo.end);
			if(this.modes.length > 1){
				throw 'Illegal';
			}
		}
	});
	
	// more utilities
	
	function replaceText(node, className, text){
		if(String(node.tagName).toLowerCase() == "code" && String(node.parentNode.tagName).toLowerCase() == "pre"){
			// See these 4 lines? This is IE's notion of "node.innerHTML = text". Love this browser :-/
			var container = document.createElement('div'),
				environment = node.parentNode.parentNode;
			container.innerHTML = '<pre><code class="' + className + '">' + text + '</code></pre>';
			environment.replaceChild(container.firstChild, node.parentNode);
		}else{
			node.className = className;
			node.innerHTML = text;
		}
	}
	function highlightStringLanguage(lang, str){
		var highlight = new Highlighter(lang, str);
		return {result:highlight.result, langName:lang, partialResult:highlight.partialResult};		
	}

	function highlightLanguage(block, lang){
		var result = highlightStringLanguage(lang, blockText(block));
		replaceText(block, block.className, result.result);
	}

	function highlightStringAuto(str){
		var result = "", langName = "", bestRelevance = 2,
			textBlock = str;
		for(var key in dh.languages){
			if(!dh.languages[key].defaultMode){ continue; }	// skip internal members
			var highlight = new Highlighter(key, textBlock),
				relevance = highlight.keywordCount + highlight.relevance, relevanceMax = 0;
			if(!result || relevance > relevanceMax){
				relevanceMax = relevance;
				result = highlight.result;
				langName = highlight.langName;
			}
		}
		return {result:result, langName:langName};
	}
	
	function highlightAuto(block){
		var result = highlightStringAuto(blockText(block));
		if(result.result){
			replaceText(block, result.langName, result.result);
		}
	}
	
	// the public API

	dojox.highlight.processString = function(/* String */ str, /* String? */lang){
		// summary: highlight a string of text
		// returns: Object containing:
		//         result - string of html with spans to apply formatting
		//         partialResult - if the formating failed: string of html
		//                 up to the point of the failure, otherwise: undefined
		//         langName - the language used to do the formatting
		return lang ? highlightStringLanguage(lang, str) : highlightStringAuto(str);
	};

	dojox.highlight.init = function(/* String|DomNode */ node){
		//	summary: Highlight a passed node
		//	
		//	description:
		//		
		//		Syntax highlight a passed DomNode or String ID of a DomNode
		//
		// 
		//	example:
		//	|	dojox.highlight.init("someId");
		//		
		node = dojo.byId(node);
		if(dojo.hasClass(node, "no-highlight")){ return; }
		if(!verifyText(node)){ return; }
	
		var classes = node.className.split(/\s+/),
			flag = dojo.some(classes, function(className){
				if(className.charAt(0) != "_" && dh.languages[className]){
					highlightLanguage(node, className);
					return true;	// stop iterations
				}
				return false;	// continue iterations
			});
		if(!flag){
			highlightAuto(node);
		}
	};

/*=====
	dojox.highlight.Code = function(props, node){
		//	summary: A Class object to allow for dojoType usage with the highlight engine. This is
		//		NOT a Widget in the conventional sense, and does not have any member functions for
		//		the instance. This is provided as a convenience. You likely should be calling
		//		`dojox.highlight.init` directly.
		//
		//	props: Object?
		//		Unused. Pass 'null' or {}. Positional usage to allow `dojo.parser` to instantiate 
		//		this class as other Widgets would be.
		// 
		//	node: String|DomNode
		//		A String ID or DomNode reference to use as the root node of this instance. 
		//
		//	example:
		//	|	<pre><code dojoType="dojox.highlight.Code">for(var i in obj){ ... }</code></pre>
		//
		//	example:
		//	|	var inst = new dojox.highlight.Code({}, "someId");
		//
		this.node = dojo.byId(node);
	};
=====*/

	dh.Code = function(p, n){ dh.init(n); };

})();

}

if(!dojo._hasResource["dojox.highlight"]){ //_hasResource checks added by build. Do not use _hasResource directly in your code.
dojo._hasResource["dojox.highlight"] = true;
dojo.provide("dojox.highlight");
 

}

if(!dojo._hasResource["dojox.highlight.languages.xml"]){ //_hasResource checks added by build. Do not use _hasResource directly in your code.
dojo._hasResource["dojox.highlight.languages.xml"] = true;
dojo.provide("dojox.highlight.languages.xml");



(function(){
	var XML_COMMENT = {
		className: 'comment',
		begin: '<!--', end: '-->'
	};
	
	var XML_ATTR = {
		className: 'attribute',
		begin: ' [a-zA-Z-]+=', end: '^',
		contains: ['value']
	};
	
	var XML_VALUE = {
		className: 'value',
		begin: '"', end: '"'
	};
	
	var dh = dojox.highlight, dhc = dh.constants;
	dh.languages.xml = {
		defaultMode: {
			contains: ['pi', 'comment', 'cdata', 'tag']
		},
		case_insensitive: true,
		modes: [
			{
				className: 'pi',
				begin: '<\\?', end: '\\?>',
				relevance: 10
			},
			XML_COMMENT,
			{
				className: 'cdata',
				begin: '<\\!\\[CDATA\\[', end: '\\]\\]>'
			},
			{
				className: 'tag',
				begin: '</?', end: '>',
				contains: ['title', 'tag_internal'],
				relevance: 1.5
			},
			{
				className: 'title',
				begin: '[A-Za-z:_][A-Za-z0-9\\._:-]+', end: '^',
				relevance: 0
			},
			{
				className: 'tag_internal',
				begin: '^', endsWithParent: true,
				contains: ['attribute'],
				relevance: 0,
				illegal: '[\\+\\.]'
			},
			XML_ATTR,
			XML_VALUE
		],
		// exporting constants
		XML_COMMENT: XML_COMMENT,
		XML_ATTR: XML_ATTR,
		XML_VALUE: XML_VALUE
	};
})();

}

if(!dojo._hasResource["dojox.highlight.languages.html"]){ //_hasResource checks added by build. Do not use _hasResource directly in your code.
dojo._hasResource["dojox.highlight.languages.html"] = true;
dojo.provide("dojox.highlight.languages.html"); 




(function(){
	var HTML_TAGS = {
		'code': 1, 'kbd': 1, 'font': 1, 'noscript': 1, 'style': 1, 'img': 1,
		'title': 1, 'menu': 1, 'tt': 1, 'tr': 1, 'param': 1, 'li': 1, 'tfoot': 1,
		'th': 1, 'input': 1, 'td': 1, 'dl': 1, 'blockquote': 1, 'fieldset': 1,
		'big': 1, 'dd': 1, 'abbr': 1, 'optgroup': 1, 'dt': 1, 'button': 1,
		'isindex': 1, 'p': 1, 'small': 1, 'div': 1, 'dir': 1, 'em': 1, 'frame': 1,
		'meta': 1, 'sub': 1, 'bdo': 1, 'label': 1, 'acronym': 1, 'sup': 1, 
		'body': 1, 'xml': 1, 'basefont': 1, 'base': 1, 'br': 1, 'address': 1,
		'strong': 1, 'legend': 1, 'ol': 1, 'script': 1, 'caption': 1, 's': 1,
		'col': 1, 'h2': 1, 'h3': 1, 'h1': 1, 'h6': 1, 'h4': 1, 'h5': 1, 'table': 1,
		'select': 1, 'noframes': 1, 'span': 1, 'area': 1, 'dfn': 1, 'strike': 1,
		'cite': 1, 'thead': 1, 'head': 1, 'option': 1, 'form': 1, 'hr': 1, 
		'var': 1, 'link': 1, 'b': 1, 'colgroup': 1, 'ul': 1, 'applet': 1, 'del': 1,
		'iframe': 1, 'pre': 1, 'frameset': 1, 'ins': 1, 'tbody': 1, 'html': 1,
		'samp': 1, 'map': 1, 'object': 1, 'a': 1, 'xmlns': 1, 'center': 1,
		'textarea': 1, 'i': 1, 'q': 1, 'u': 1
	};
	var HTML_DOCTYPE = {
		className: 'doctype',
		begin: '<!DOCTYPE', end: '>',
		relevance: 10
	};
	var HTML_ATTR = {
		className: 'attribute',
		begin: ' [a-zA-Z]+', end: '^'
	};
	var HTML_VALUE = {
		className: 'value',
		begin: '[a-zA-Z0-9]+', end: '^'
	};

	var dh = dojox.highlight, dhc = dh.constants, dhl = dh.languages, x = dhl.xml;
	dhl.html = {
		defaultMode: {
			contains: ['tag', 'comment', 'doctype']
		},
		case_insensitive: true,
		modes: [
			x.XML_COMMENT,
			HTML_DOCTYPE,
			{
				className: 'tag',
				lexems: [dhc.IDENT_RE],
				keywords: HTML_TAGS,
				begin: '<[A-Za-z/]', end: '>',
				contains: ['attribute'],
				illegal: '[\\+\\.]'
			},
			x.XML_ATTR,
			HTML_ATTR,
			x.XML_VALUE,
			HTML_VALUE
		],
		// exporting constants
		HTML_TAGS: HTML_TAGS,
		HTML_DOCTYPE: HTML_DOCTYPE,
		HTML_ATTR: HTML_ATTR,
		HTML_VALUE: HTML_VALUE
	};
})();

}

if(!dojo._hasResource["dojox.highlight.languages.css"]){ //_hasResource checks added by build. Do not use _hasResource directly in your code.
dojo._hasResource["dojox.highlight.languages.css"] = true;
dojo.provide("dojox.highlight.languages.css"); 




(function(){
	var dh = dojox.highlight, dhc = dh.constants, dhl = dh.languages;
	dhl.css = {
		defaultMode: {
			contains: ['id', 'class', 'attr_selector', 'rules', 'comment'],
			keywords: dhl.html.HTML_TAGS,
			lexems: [dhc.IDENT_RE],
			illegal: '='
		},
		case_insensitive: true,
		modes: [
			{
				className: 'id',
				begin: '\\#[A-Za-z0-9_-]+', end: '^'
			},
			{
				className: 'class',
				begin: '\\.[A-Za-z0-9_-]+', end: '^',
				relevance: 0
			},
			{
				className: 'attr_selector',
				begin: '\\[', end: '\\]',
				illegal: '$'
			},
			{
				className: 'rules',
				begin: '{', end: '}',
				lexems: ['[A-Za-z-]+'],
				keywords: {
					'play-during': 1, 'counter-reset': 1, 
					'counter-increment': 1, 'min-height': 1, 'quotes': 1,
					'border-top': 1, 'pitch': 1, 'font': 1, 'pause': 1,
					'list-style-image': 1, 'border-width': 1, 'cue': 1,
					'outline-width': 1, 'border-left': 1, 'elevation': 1,
					'richness': 1, 'speech-rate': 1, 'border-bottom': 1,
					'border-spacing': 1, 'background': 1, 'list-style-type': 1,
					'text-align': 1, 'page-break-inside': 1, 'orphans': 1,
					'page-break-before': 1, 'text-transform': 1, 
					'line-height': 1, 'padding-left': 1, 'font-size': 1,
					'right': 1, 'word-spacing': 1, 'padding-top': 1,
					'outline-style': 1, 'bottom': 1, 'content': 1,
					'border-right-style': 1, 'padding-right': 1,
					'border-left-style': 1, 'voice-family': 1,
					'background-color': 1, 'border-bottom-color': 1,
					'outline-color': 1, 'unicode-bidi': 1, 'max-width': 1,
					'font-family': 1, 'caption-side': 1, 
					'border-right-width': 1, 'pause-before': 1,
					'border-top-style': 1, 'color': 1, 'border-collapse': 1,
					'border-bottom-width': 1, 'float': 1, 'height': 1,
					'max-height': 1, 'margin-right': 1, 'border-top-width': 1,
					'speak': 1, 'speak-header': 1, 'top': 1, 'cue-before': 1,
					'min-width': 1, 'width': 1, 'font-variant': 1,
					'border-top-color': 1, 'background-position': 1,
					'empty-cells': 1, 'direction': 1, 'border-right': 1,
					'visibility': 1, 'padding': 1, 'border-style': 1,
					'background-attachment': 1, 'overflow': 1,
					'border-bottom-style': 1, 'cursor': 1, 'margin': 1,
					'display': 1, 'border-left-width': 1, 'letter-spacing': 1,
					'vertical-align': 1, 'clip': 1, 'border-color': 1,
					'list-style': 1, 'padding-bottom': 1, 'pause-after': 1,
					'speak-numeral': 1, 'margin-left': 1, 'widows': 1,
					'border': 1, 'font-style': 1, 'border-left-color': 1,
					'pitch-range': 1, 'background-repeat': 1, 
					'table-layout': 1, 'margin-bottom': 1, 
					'speak-punctuation': 1, 'font-weight': 1,
					'border-right-color': 1, 'page-break-after': 1, 
					'position': 1, 'white-space': 1, 'text-indent': 1,
					'background-image': 1, 'volume': 1, 'stress': 1, 
					'outline': 1, 'clear': 1, 'z-index': 1, 
					'text-decoration': 1, 'margin-top': 1, 'azimuth': 1,
					'cue-after': 1, 'left': 1, 'list-style-position': 1
				},
				contains: ['comment', 'value']
			},
			dhc.C_BLOCK_COMMENT_MODE,
			{
				className: 'value',
				begin: ':', 
				end: ';', 
				endsWithParent: true, 
				excludeBegin: true, 
				excludeEnd: true
			}
		]
	};
})();

}

if(!dojo._hasResource["dojox.highlight.languages.django"]){ //_hasResource checks added by build. Do not use _hasResource directly in your code.
dojo._hasResource["dojox.highlight.languages.django"] = true;
dojo.provide("dojox.highlight.languages.django"); 





(function(){ 
	var dh = dojox.highlight, dhc = dh.constants, dhl = dh.languages, x = dhl.xml, h = dhl.html;
	dhl.django = {
		defaultMode: {
			contains: ['tag', 'comment', 'doctype', 'template_comment', 'template_tag', 'variable']
		},
		case_insensitive: true,
		modes: [
			x.XML_COMMENT,
			h.HTML_DOCTYPE,
			{
				className: 'tag',
				lexems: [dhc.IDENT_RE],
				keywords: h.HTML_TAGS,
				begin: '<[A-Za-z/]', end: '>',
				contains: ['attribute', 'template_comment', 'template_tag', 'variable']
			},
			x.XML_ATTR,
			h.HTML_ATTR,
			{
				className: 'value',
				begin: '"', end: '"',
				contains: ['template_comment', 'template_tag', 'variable']
			},
			h.HTML_VALUE,
			{
				className: 'template_comment',
				begin: '\\{\\%\\s*comment\\s*\\%\\}', 
				end: '\\{\\%\\s*endcomment\\s*\\%\\}'
			},
			{
				className: 'template_comment',
				begin: '\\{#', end: '#\\}'
			},
			{
				className: 'template_tag',
				begin: '\\{\\%', end: '\\%\\}',
				lexems: [dhc.IDENT_RE],
				keywords: {
					'comment': 1, 'endcomment': 1, 'load': 1,
					'templatetag': 1, 'ifchanged': 1, 'endifchanged': 1,
					'if': 1, 'endif': 1, 'firstof': 1, 'for': 1, 
					'endfor': 1, 'in': 1, 'ifnotequal': 1, 
					'endifnotequal': 1, 'widthratio': 1, 'extends': 1,
					'include': 1, 'spaceless': 1, 'endspaceless': 1,
					'regroup': 1, 'by': 1, 'as': 1, 'ifequal': 1,
					'endifequal': 1, 'ssi': 1, 'now': 1, 'with': 1,
					'cycle': 1, 'url': 1, 'filter': 1, 'endfilter': 1,
					'debug': 1, 'block': 1, 'endblock': 1, 'else': 1
				},
				contains: ['filter']
			},
			{
				className: 'variable',
				begin: '\\{\\{', end: '\\}\\}',
				contains: ['filter']
			},
			{
				className: 'filter',
				begin: '\\|[A-Za-z]+\\:?', end: '^', excludeEnd: true,
				lexems: [dhc.IDENT_RE],
				keywords: {
					'truncatewords': 1, 'removetags': 1, 'linebreaksbr': 1,
					'yesno': 1, 'get_digit': 1, 'timesince': 1, 'random': 1,
					'striptags': 1, 'filesizeformat': 1, 'escape': 1,
					'linebreaks': 1, 'length_is': 1, 'ljust': 1, 'rjust': 1,
					'cut': 1, 'urlize': 1, 'fix_ampersands': 1, 'title': 1,
					'floatformat': 1, 'capfirst': 1, 'pprint': 1,
					'divisibleby': 1, 'add': 1, 'make_list': 1,
					'unordered_list': 1, 'urlencode': 1, 'timeuntil': 1,
					'urlizetrunc': 1, 'wordcount': 1, 'stringformat': 1,
					'linenumbers': 1, 'slice': 1, 'date': 1, 'dictsort': 1,
					'dictsortreversed': 1, 'default_if_none': 1, 
					'pluralize': 1, 'lower': 1, 'join': 1, 'center': 1,
					'default': 1, 'truncatewords_html': 1, 'upper': 1,
					'length': 1, 'phone2numeric': 1, 'wordwrap': 1, 'time': 1,
					'addslashes': 1, 'slugify': 1, 'first': 1
				},
				contains: ['argument']
			},
			{
				className: 'argument',
				begin: '"', end: '"'
			}
		]
	};
})();

}

if(!dojo._hasResource["dojox.highlight.languages.javascript"]){ //_hasResource checks added by build. Do not use _hasResource directly in your code.
dojo._hasResource["dojox.highlight.languages.javascript"] = true;
dojo.provide("dojox.highlight.languages.javascript");



(function(){
	var dh = dojox.highlight, dhc = dh.constants;
	dh.languages.javascript = {
		defaultMode: {
			lexems: [dhc.UNDERSCORE_IDENT_RE],
			contains: ['string', 'comment', 'number', 'regexp', 'function'],
			keywords: {
				'keyword': {
					'in': 1, 'if': 1, 'for': 1, 'while': 1, 'finally': 1, 'var': 1,
					'new': 1, 'function': 1, 'do': 1, 'return': 1, 'void': 1,
					'else': 1, 'break': 1, 'catch': 1, 'instanceof': 1, 'with': 1,
					'throw': 1, 'case': 1, 'default': 1, 'try': 1, 'this': 1,
					'switch': 1, 'continue': 1, 'typeof': 1, 'delete': 1
				},
				'literal': {'true': 1, 'false': 1, 'null': 1}
			}
		},
		modes: [
			dhc.C_LINE_COMMENT_MODE,
			dhc.C_BLOCK_COMMENT_MODE,
			dhc.C_NUMBER_MODE,
			dhc.APOS_STRING_MODE,
			dhc.QUOTE_STRING_MODE,
			dhc.BACKSLASH_ESCAPE,
			{
				className: 'regexp',
				begin: '/.*?[^\\\\/]/[gim]*', end: '^'
			},
			{
				className: 'function',
				begin: 'function\\b', end: '{',
				lexems: [dhc.UNDERSCORE_IDENT_RE],
				keywords: {'function': 1},
				contains: ['title', 'params']
			},
			{
				className: 'title',
				begin: dhc.UNDERSCORE_IDENT_RE, end: '^'
			},
			{
				className: 'params',
				begin: '\\(', end: '\\)',
				contains: ['string', 'comment']
			}
		]
	};
})();

}

if(!dojo._hasResource["dojox.highlight.languages._www"]){ //_hasResource checks added by build. Do not use _hasResource directly in your code.
dojo._hasResource["dojox.highlight.languages._www"] = true;
dojo.provide("dojox.highlight.languages._www");

/* common web-centric languages */






}

if(!dojo._hasResource["dojox.highlight.languages.pygments.xml"]){ //_hasResource checks added by build. Do not use _hasResource directly in your code.
dojo._hasResource["dojox.highlight.languages.pygments.xml"] = true;
dojo.provide("dojox.highlight.languages.pygments.xml");


dojox.highlight.languages.pygments.xml = {a: 1};
dojox.highlight.languages.xml = {
	defaultMode: {
		contains: [
			"name entity",
			"comment", "comment preproc",
			"_tag"
		]
	},
	modes: [
		// comments
		{
			className: "comment",
			begin: "<!--", end: "-->"
		},
		{
			className: "comment preproc",
			begin: "\\<\\!\\[CDATA\\[", end: "\\]\\]\\>"
		},
		{
			className: "comment preproc",
			begin: "\\<\\!", end: "\\>"
		},
		{
			className: "comment preproc",
			begin: "\\<\\?", end: "\\?\\>",
			relevance: 5
		},

		// strings
		{
			className: "string",
			begin: "'", end: "'",
			illegal: "\\n",
			relevance: 0
		},
		{
			className: "string",
			begin: '"', 
			end: '"',
			illegal: "\\n",
			relevance: 0
		},
		
		// names
		{
			className: "name entity",
			begin: "\\&[a-z]+;", end: "^"
		},
		{
			className: "name tag",
			begin: "\\b[a-z0-9_\\:\\-]+\\b", end: "^"
		},
		{
			className: "name attribute",
			begin: "\\b[a-z0-9_\\:\\-]+=", end: "^",
			relevance: 0
		},
		
		
		{
			className: "_tag",
			begin: "\\<", end: "\\>",
			contains: ["name tag", "name attribute", "string"]
		},
		{
			className: "_tag",
			begin: "\\</", end: "\\>",
			contains: ["name tag"]
		}
	]
};

}

if(!dojo._hasResource["dojox.highlight.languages.pygments._html"]){ //_hasResource checks added by build. Do not use _hasResource directly in your code.
dojo._hasResource["dojox.highlight.languages.pygments._html"] = true;
dojo.provide("dojox.highlight.languages.pygments._html");

// html-related constants

dojox.highlight.languages.pygments._html.tags = {
	"code": 1, "kbd": 1, "font": 1, "noscript": 1, "style": 1, "img": 1,
	"title": 1, "menu": 1, "tt": 1, "tr": 1, "param": 1, "li": 1, "tfoot": 1,
	"th": 1, "input": 1, "td": 1, "dl": 1, "blockquote": 1, "fieldset": 1,
	"big": 1, "dd": 1, "abbr": 1, "optgroup": 1, "dt": 1, "button": 1,
	"isindex": 1, "p": 1, "small": 1, "div": 1, "dir": 1, "em": 1, "frame": 1,
	"meta": 1, "sub": 1, "bdo": 1, "label": 1, "acronym": 1, "sup": 1, 
	"body": 1, "xml": 1, "basefont": 1, "base": 1, "br": 1, "address": 1,
	"strong": 1, "legend": 1, "ol": 1, "script": 1, "caption": 1, "s": 1,
	"col": 1, "h2": 1, "h3": 1, "h1": 1, "h6": 1, "h4": 1, "h5": 1, "table": 1,
	"select": 1, "noframes": 1, "span": 1, "area": 1, "dfn": 1, "strike": 1,
	"cite": 1, "thead": 1, "head": 1, "option": 1, "form": 1, "hr": 1, 
	"var": 1, "link": 1, "b": 1, "colgroup": 1, "ul": 1, "applet": 1, "del": 1,
	"iframe": 1, "pre": 1, "frameset": 1, "ins": 1, "tbody": 1, "html": 1,
	"samp": 1, "map": 1, "object": 1, "a": 1, "xmlns": 1, "center": 1,
	"textarea": 1, "i": 1, "q": 1, "u": 1
};

}

if(!dojo._hasResource["dojox.highlight.languages.pygments.html"]){ //_hasResource checks added by build. Do not use _hasResource directly in your code.
dojo._hasResource["dojox.highlight.languages.pygments.html"] = true;
dojo.provide("dojox.highlight.languages.pygments.html");




(function(){
	var dh = dojox.highlight, dhl = dh.languages, tags = [],
		ht = dhl.pygments._html.tags;
	
	for(var key in ht){
		tags.push(key);
	}
	tags = "\\b(" + tags.join("|") + ")\\b";
	
	dhl.html = {
		case_insensitive: true,
		defaultMode: {
			contains: [
				"name entity",
				"comment", "comment preproc",
				"_script", "_style", "_tag"
			]
		},
		modes: [
			// comments
			{
				className: "comment",
				begin: "<!--", end: "-->"
			},
			{
				className: "comment preproc",
				begin: "\\<\\!\\[CDATA\\[", end: "\\]\\]\\>"
			},
			{
				className: "comment preproc",
				begin: "\\<\\!", end: "\\>"
			},

			// strings
			{
				className: "string",
				begin: "'", end: "'",
				illegal: "\\n",
				relevance: 0
			},
			{
				className: "string",
				begin: '"', 
				end: '"',
				illegal: "\\n",
				relevance: 0
			},
			
			// names
			{
				className: "name entity",
				begin: "\\&[a-z]+;", end: "^"
			},
			{
				className: "name tag",
				begin: tags, end: "^",
				relevance: 5
			},
			{
				className: "name attribute",
				begin: "\\b[a-z0-9_\\:\\-]+\\s*=", end: "^",
				relevance: 0
			},
			
			{
				className: "_script",
				begin: "\\<script\\b", end: "\\</script\\>",
				relevance: 5
			},
			{
				className: "_style",
				begin: "\\<style\\b", end: "\\</style\\>",
				relevance: 5
			},
			
			{
				className: "_tag",
				begin: "\\<(?!/)", end: "\\>",
				contains: ["name tag", "name attribute", "string", "_value"]
			},
			{
				className: "_tag",
				begin: "\\</", end: "\\>",
				contains: ["name tag"]
			},
			{
				className: "_value",
				begin: "[^\\s\\>]+", end: "^"
			}
		]
	};
})();

}

if(!dojo._hasResource["dojox.highlight.languages.pygments.css"]){ //_hasResource checks added by build. Do not use _hasResource directly in your code.
dojo._hasResource["dojox.highlight.languages.pygments.css"] = true;
dojo.provide("dojox.highlight.languages.pygments.css");




(function(){
	var dh = dojox.highlight, dhl = dh.languages;
	dhl.css = {
		defaultMode: {
			lexems: ["\\b[a-zA-Z0-9]+\\b", "\\b@media\b"],
			keywords: {
				"keyword": {
					"@media": 1
				},
				"name tag": dhl.pygments._html.tags
			},
			contains: [
				"comment",
				"string single", "string double",
				"punctuation",
				"name decorator", "name class", "name function",
				"_content"
			]
		},
		modes: [
			// comments
			{
				className: "comment",
				begin: "/\\*", end: "\\*/",
				relevance: 0
			},
			{
				className: "comment preproc",
				begin: "@[a-z][a-zA-Z]*", end: "^"
			},
			{
				className: "comment preproc",
				begin: "\\!important\\b", end: "^"
			},

			// numbers
			{
				className: "number",
				begin: "\\#[a-fA-F0-9]{3}\\b", end: "^",
				relevance: 0
			},
			{
				className: "number",
				begin: "\\#[a-fA-F0-9]{6}\\b", end: "^",
				relevance: 0
			},
			{
				className: "number",
				begin: "[\\.\\-]?[0-9]*[\\.]?[0-9]+(em|px|\\%|pt|pc|in|mm|cm|ex)", end: "^",
				relevance: 0
			},
			{
				className: "number",
				begin: "\\-?[0-9]+", end: "^",
				relevance: 0
			},

			// strings
			{
				className: "string single",
				begin: "'", end: "'",
				illegal: "\\n",
				relevance: 0
			},
			{
				className: "string double",
				begin: '"', 
				end: '"',
				illegal: "\\n",
				relevance: 0
			},
			
			// operators
			{
				className: "operator",
				begin: "[~\\^\\*!%&\\[\\]\\(\\)<>\\|+=@:;,./?-]", end: "^",
				relevance: 0
			},

			// punctuations
			{
				className: "punctuation",
				begin: "[\\[\\]();]+", end: "^",
				relevance: 0
			},
			
			// names
			{
				className: "name decorator",
				begin: "\\:[a-zA-Z0-9_\\-]+\\b", end: "^"
			},
			{
				className: "name class",
				begin: "\\.[a-zA-Z0-9_\\-]+\\b", end: "^"
			},
			{
				className: "name function",
				begin: "\\#[a-zA-Z0-9_\\-]+\\b", end: "^"
			},
			{
				className: "_content",
				begin: "\\{", end: "\\}",
				lexems: ["\\b[a-zA-Z\\-]+\\b"],
				keywords: {
					"keyword": {
						"azimuth": 1, "background-attachment": 1, "background-color": 1,
						"background-image": 1, "background-position": 1, "background-repeat": 1,
						"background": 1, "border-bottom-color": 1, "border-bottom-style": 1,
						"border-bottom-width": 1, "border-left-color": 1, "border-left-style": 1,
						"border-left-width": 1, "border-right": 1, "border-right-color": 1,
						"border-right-style": 1, "border-right-width": 1, "border-top-color": 1,
						"border-top-style": 1, "border-top-width": 1, "border-bottom": 1,
						"border-collapse": 1, "border-left": 1, "border-width": 1, "border-color": 1,
						"border-spacing": 1, "border-style": 1, "border-top": 1, "border": 1, "caption-side": 1,
						"clear": 1, "clip": 1, "color": 1, "content": 1, "counter-increment": 1, "counter-reset": 1,
						"cue-after": 1, "cue-before": 1, "cue": 1, "cursor": 1, "direction": 1, "display": 1,
						"elevation": 1, "empty-cells": 1, "float": 1, "font-family": 1, "font-size": 1,
						"font-size-adjust": 1, "font-stretch": 1, "font-style": 1, "font-variant": 1,
						"font-weight": 1, "font": 1, "height": 1, "letter-spacing": 1, "line-height": 1,
						"list-style-type": 1, "list-style-image": 1, "list-style-position": 1,
						"list-style": 1, "margin-bottom": 1, "margin-left": 1, "margin-right": 1,
						"margin-top": 1, "margin": 1, "marker-offset": 1, "marks": 1, "max-height": 1, "max-width": 1,
						"min-height": 1, "min-width": 1, "opacity": 1, "orphans": 1, "outline": 1, "outline-color": 1,
						"outline-style": 1, "outline-width": 1, "overflow": 1, "padding-bottom": 1,
						"padding-left": 1, "padding-right": 1, "padding-top": 1, "padding": 1, "page": 1,
						"page-break-after": 1, "page-break-before": 1, "page-break-inside": 1,
						"pause-after": 1, "pause-before": 1, "pause": 1, "pitch": 1, "pitch-range": 1,
						"play-during": 1, "position": 1, "quotes": 1, "richness": 1, "right": 1, "size": 1,
						"speak-header": 1, "speak-numeral": 1, "speak-punctuation": 1, "speak": 1,
						"speech-rate": 1, "stress": 1, "table-layout": 1, "text-align": 1, "text-decoration": 1,
						"text-indent": 1, "text-shadow": 1, "text-transform": 1, "top": 1, "unicode-bidi": 1,
						"vertical-align": 1, "visibility": 1, "voice-family": 1, "volume": 1, "white-space": 1,
						"widows": 1, "width": 1, "word-spacing": 1, "z-index": 1, "bottom": 1, "left": 1,
						"above": 1, "absolute": 1, "always": 1, "armenian": 1, "aural": 1, "auto": 1, "avoid": 1, "baseline": 1,
						"behind": 1, "below": 1, "bidi-override": 1, "blink": 1, "block": 1, "bold": 1, "bolder": 1, "both": 1,
						"capitalize": 1, "center-left": 1, "center-right": 1, "center": 1, "circle": 1,
						"cjk-ideographic": 1, "close-quote": 1, "collapse": 1, "condensed": 1, "continuous": 1,
						"crop": 1, "crosshair": 1, "cross": 1, "cursive": 1, "dashed": 1, "decimal-leading-zero": 1,
						"decimal": 1, "default": 1, "digits": 1, "disc": 1, "dotted": 1, "double": 1, "e-resize": 1, "embed": 1,
						"extra-condensed": 1, "extra-expanded": 1, "expanded": 1, "fantasy": 1, "far-left": 1,
						"far-right": 1, "faster": 1, "fast": 1, "fixed": 1, "georgian": 1, "groove": 1, "hebrew": 1, "help": 1,
						"hidden": 1, "hide": 1, "higher": 1, "high": 1, "hiragana-iroha": 1, "hiragana": 1, "icon": 1,
						"inherit": 1, "inline-table": 1, "inline": 1, "inset": 1, "inside": 1, "invert": 1, "italic": 1,
						"justify": 1, "katakana-iroha": 1, "katakana": 1, "landscape": 1, "larger": 1, "large": 1,
						"left-side": 1, "leftwards": 1, "level": 1, "lighter": 1, "line-through": 1, "list-item": 1,
						"loud": 1, "lower-alpha": 1, "lower-greek": 1, "lower-roman": 1, "lowercase": 1, "ltr": 1,
						"lower": 1, "low": 1, "medium": 1, "message-box": 1, "middle": 1, "mix": 1, "monospace": 1,
						"n-resize": 1, "narrower": 1, "ne-resize": 1, "no-close-quote": 1, "no-open-quote": 1,
						"no-repeat": 1, "none": 1, "normal": 1, "nowrap": 1, "nw-resize": 1, "oblique": 1, "once": 1,
						"open-quote": 1, "outset": 1, "outside": 1, "overline": 1, "pointer": 1, "portrait": 1, "px": 1,
						"relative": 1, "repeat-x": 1, "repeat-y": 1, "repeat": 1, "rgb": 1, "ridge": 1, "right-side": 1,
						"rightwards": 1, "s-resize": 1, "sans-serif": 1, "scroll": 1, "se-resize": 1,
						"semi-condensed": 1, "semi-expanded": 1, "separate": 1, "serif": 1, "show": 1, "silent": 1,
						"slow": 1, "slower": 1, "small-caps": 1, "small-caption": 1, "smaller": 1, "soft": 1, "solid": 1,
						"spell-out": 1, "square": 1, "static": 1, "status-bar": 1, "super": 1, "sw-resize": 1,
						"table-caption": 1, "table-cell": 1, "table-column": 1, "table-column-group": 1,
						"table-footer-group": 1, "table-header-group": 1, "table-row": 1,
						"table-row-group": 1, "text": 1, "text-bottom": 1, "text-top": 1, "thick": 1, "thin": 1,
						"transparent": 1, "ultra-condensed": 1, "ultra-expanded": 1, "underline": 1,
						"upper-alpha": 1, "upper-latin": 1, "upper-roman": 1, "uppercase": 1, "url": 1,
						"visible": 1, "w-resize": 1, "wait": 1, "wider": 1, "x-fast": 1, "x-high": 1, "x-large": 1, "x-loud": 1,
						"x-low": 1, "x-small": 1, "x-soft": 1, "xx-large": 1, "xx-small": 1, "yes": 1
					},
					"name builtin": {
						"indigo": 1, "gold": 1, "firebrick": 1, "indianred": 1, "yellow": 1, "darkolivegreen": 1,
						"darkseagreen": 1, "mediumvioletred": 1, "mediumorchid": 1, "chartreuse": 1,
						"mediumslateblue": 1, "black": 1, "springgreen": 1, "crimson": 1, "lightsalmon": 1, "brown": 1,
						"turquoise": 1, "olivedrab": 1, "cyan": 1, "silver": 1, "skyblue": 1, "gray": 1, "darkturquoise": 1,
						"goldenrod": 1, "darkgreen": 1, "darkviolet": 1, "darkgray": 1, "lightpink": 1, "teal": 1,
						"darkmagenta": 1, "lightgoldenrodyellow": 1, "lavender": 1, "yellowgreen": 1, "thistle": 1,
						"violet": 1, "navy": 1, "orchid": 1, "blue": 1, "ghostwhite": 1, "honeydew": 1, "cornflowerblue": 1,
						"darkblue": 1, "darkkhaki": 1, "mediumpurple": 1, "cornsilk": 1, "red": 1, "bisque": 1, "slategray": 1,
						"darkcyan": 1, "khaki": 1, "wheat": 1, "deepskyblue": 1, "darkred": 1, "steelblue": 1, "aliceblue": 1,
						"gainsboro": 1, "mediumturquoise": 1, "floralwhite": 1, "coral": 1, "purple": 1, "lightgrey": 1,
						"lightcyan": 1, "darksalmon": 1, "beige": 1, "azure": 1, "lightsteelblue": 1, "oldlace": 1,
						"greenyellow": 1, "royalblue": 1, "lightseagreen": 1, "mistyrose": 1, "sienna": 1,
						"lightcoral": 1, "orangered": 1, "navajowhite": 1, "lime": 1, "palegreen": 1, "burlywood": 1,
						"seashell": 1, "mediumspringgreen": 1, "fuchsia": 1, "papayawhip": 1, "blanchedalmond": 1,
						"peru": 1, "aquamarine": 1, "white": 1, "darkslategray": 1, "ivory": 1, "dodgerblue": 1,
						"lemonchiffon": 1, "chocolate": 1, "orange": 1, "forestgreen": 1, "slateblue": 1, "olive": 1,
						"mintcream": 1, "antiquewhite": 1, "darkorange": 1, "cadetblue": 1, "moccasin": 1,
						"limegreen": 1, "saddlebrown": 1, "darkslateblue": 1, "lightskyblue": 1, "deeppink": 1,
						"plum": 1, "aqua": 1, "darkgoldenrod": 1, "maroon": 1, "sandybrown": 1, "magenta": 1, "tan": 1,
						"rosybrown": 1, "pink": 1, "lightblue": 1, "palevioletred": 1, "mediumseagreen": 1,
						"dimgray": 1, "powderblue": 1, "seagreen": 1, "snow": 1, "mediumblue": 1, "midnightblue": 1,
						"paleturquoise": 1, "palegoldenrod": 1, "whitesmoke": 1, "darkorchid": 1, "salmon": 1,
						"lightslategray": 1, "lawngreen": 1, "lightgreen": 1, "tomato": 1, "hotpink": 1,
						"lightyellow": 1, "lavenderblush": 1, "linen": 1, "mediumaquamarine": 1, "green": 1,
						"blueviolet": 1, "peachpuff": 1
					}
				},
				contains: [
					"comment", "comment preproc", 
					"number",
					"string single", "string double",
					"punctuation",
					"name decorator", "name class", "name function"
				]
			}
		]
	};
})();

}

if(!dojo._hasResource["dojox.highlight.languages.pygments.javascript"]){ //_hasResource checks added by build. Do not use _hasResource directly in your code.
dojo._hasResource["dojox.highlight.languages.pygments.javascript"] = true;
dojo.provide("dojox.highlight.languages.pygments.javascript");



(function(){
	var dh = dojox.highlight, dhc = dh.constants;
	dh.languages.javascript = {
		defaultMode: {
			lexems: ["\\b[a-zA-Z]+"],
			keywords: {
				"keyword": {
					"for": 1, "in": 1, "while": 1, "do": 1, "break": 1, "return": 1,
					"continue": 1, "if": 1, "else": 1, "throw": 1, "try": 1,
		            "catch": 1, "var": 1, "with": 1, "const": 1, "label": 1,
					"function": 1, "new": 1, "typeof": 1, "instanceof": 1
				},
				"keyword constant": {
					"true": 1, "false": 1, "null": 1, "NaN": 1, "Infinity": 1, "undefined": 1
				},
				"name builtin": {
					"Array": 1, "Boolean": 1, "Date": 1, "Error": 1, "Function": 1, "Math": 1,
					"netscape": 1, "Number": 1, "Object": 1, "Packages": 1, "RegExp": 1,
					"String": 1, "sun": 1, "decodeURI": 1, "decodeURIComponent": 1, 
					"encodeURI": 1, "encodeURIComponent": 1, "Error": 1, "eval": 1, 
					"isFinite": 1, "isNaN": 1, "parseFloat": 1, "parseInt": 1, "document": 1,
					"window": 1
				},
				"name builtin pseudo": {
					"this": 1
				}
			},
			contains: [
				"comment single", "comment multiline", 
				"number integer", "number oct", "number hex", "number float",
				"string single", "string double", "string regex",
				"operator",
				"punctuation",
				//"name variable",
				"_function"
			]
		},
		modes: [
			// comments
			{
				className: "comment single",
				begin: "//", end: "$",
				relevance: 0
			},
			{
				className: "comment multiline",
				begin: "/\\*", end: "\\*/"
			},

			// numbers
			{
				className: "number integer",
				begin: "0|([1-9][0-9]*)", end: "^",
				relevance: 0
			},
			{
				className: "number oct",
				begin: "0[0-9]+", end: "^",
				relevance: 0
			},
			{
				className: "number hex",
				begin: "0x[0-9a-fA-F]+", end: "^",
				relevance: 0
			},
			{
				className: "number float",
				begin: "([1-9][0-9]*\\.[0-9]*([eE][\\+-]?[0-9]+)?)|(\\.[0-9]+([eE][\\+-]?[0-9]+)?)|([0-9]+[eE][\\+-]?[0-9]+)", end: "^",
				relevance: 0
			},

			// strings
			{
				className: "string single",
				begin: "'", end: "'",
				illegal: "\\n",
				contains: ["string escape"],
				relevance: 0
			},
			{
				className: "string double",
				begin: '"', 
				end: '"',
				illegal: "\\n",
				contains: ["string escape"],
				relevance: 0
			},
			{
				className: "string escape",
				begin: "\\\\.", end: "^",
				relevance: 0
			},
			{
				className: "string regex",
				begin: "/.*?[^\\\\/]/[gim]*", end: "^"
			},
			
			// operators
			{
				className: "operator",
				begin: "\\|\\||&&|\\+\\+|--|-=|\\+=|/=|\\*=|==|[-\\+\\*/=\\?:~\\^]", end: "^",
				relevance: 0
			},

			// punctuations
			{
				className: "punctuation",
				begin: "[{}\\(\\)\\[\\]\\.;]", end: "^",
				relevance: 0
			},
			
			// functions
			{
				className: "_function",
				begin: "function\\b", end: "{",
				lexems: [dhc.UNDERSCORE_IDENT_RE],
				keywords: {
					keyword: {
						"function": 1
					}
				},
				contains: ["name function", "_params"],
				relevance: 5
			},
			{
				className: "name function",
				begin: dhc.UNDERSCORE_IDENT_RE, end: '^'
			},
			{
				className: "_params",
				begin: "\\(", end: "\\)",
				contains: ["comment single", "comment multiline"]
			}
			/*
			// names
			{
				className: "name variable",
				begin: "\\b[$a-zA-Z_][$a-zA-Z0-9_]*", end: "^",
				relevance: 0
			}
			*/
		]
	};
})();

}

if(!dojo._hasResource["dojox.highlight.languages.pygments._www"]){ //_hasResource checks added by build. Do not use _hasResource directly in your code.
dojo._hasResource["dojox.highlight.languages.pygments._www"] = true;
dojo.provide("dojox.highlight.languages.pygments._www");

/* common web-centric languages */



//dojo.require("dojox.highlight.languages.pygments.django");


}

if(!dojo._hasResource["lucidsite.documentation._base"]){ //_hasResource checks added by build. Do not use _hasResource directly in your code.
dojo._hasResource["lucidsite.documentation._base"] = true;
dojo.provide("lucidsite.documentation._base");




var initCode = function(){
	dojo.query("code").forEach(function(node) {
	    node.innerHTML = node.innerHTML.replace(/\</gi,"&lt;").replace(/\</gi,"&gt;").replace(/\&/gi,"&amp;")
	    dojox.highlight.init(node);
	});
};	
dojo.addOnLoad(initCode); 

}

if(!dojo._hasResource["lucidsite.documentation"]){ //_hasResource checks added by build. Do not use _hasResource directly in your code.
dojo._hasResource["lucidsite.documentation"] = true;
dojo.provide("lucidsite.documentation");


}

