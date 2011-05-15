// lib/handlebars/parser.js
/* Jison generated parser */var handlebars=function(){var a={trace:function(){},yy:{},symbols_:{error:2,root:3,program:4,EOF:5,statements:6,simpleInverse:7,statement:8,openInverse:9,closeBlock:10,openBlock:11,mustache:12,partial:13,CONTENT:14,COMMENT:15,OPEN_BLOCK:16,inMustache:17,CLOSE:18,OPEN_INVERSE:19,OPEN_ENDBLOCK:20,path:21,OPEN:22,OPEN_UNESCAPED:23,OPEN_PARTIAL:24,params:25,hash:26,param:27,STRING:28,hashSegments:29,hashSegment:30,ID:31,EQUALS:32,pathSegments:33,SEP:34,$accept:0,$end:1},terminals_:{2:"error",5:"EOF",14:"CONTENT",15:"COMMENT",16:"OPEN_BLOCK",18:"CLOSE",19:"OPEN_INVERSE",20:"OPEN_ENDBLOCK",22:"OPEN",23:"OPEN_UNESCAPED",24:"OPEN_PARTIAL",28:"STRING",31:"ID",32:"EQUALS",34:"SEP"},productions_:[0,[3,2],[4,3],[4,1],[4,0],[6,1],[6,2],[8,3],[8,3],[8,1],[8,1],[8,1],[8,1],[11,3],[9,3],[10,3],[12,3],[12,3],[13,3],[13,4],[7,2],[17,3],[17,2],[17,2],[17,1],[25,2],[25,1],[27,1],[27,1],[26,1],[29,2],[29,1],[30,3],[30,3],[21,1],[33,3],[33,1]],performAction:function(b,c,d,e,f,g,h){var i=g.length-1;switch(f){case 1:return g[i-1];case 2:this.$=new e.ProgramNode(g[i-2],g[i]);break;case 3:this.$=new e.ProgramNode(g[i]);break;case 4:this.$=new e.ProgramNode([]);break;case 5:this.$=[g[i]];break;case 6:g[i-1].push(g[i]),this.$=g[i-1];break;case 7:this.$=new e.InverseNode(g[i-2],g[i-1],g[i]);break;case 8:this.$=new e.BlockNode(g[i-2],g[i-1],g[i]);break;case 9:this.$=g[i];break;case 10:this.$=g[i];break;case 11:this.$=new e.ContentNode(g[i]);break;case 12:this.$=new e.CommentNode(g[i]);break;case 13:this.$=new e.MustacheNode(g[i-1][0],g[i-1][1]);break;case 14:this.$=new e.MustacheNode(g[i-1][0],g[i-1][1]);break;case 15:this.$=g[i-1];break;case 16:this.$=new e.MustacheNode(g[i-1][0],g[i-1][1]);break;case 17:this.$=new e.MustacheNode(g[i-1][0],g[i-1][1],!0);break;case 18:this.$=new e.PartialNode(g[i-1]);break;case 19:this.$=new e.PartialNode(g[i-2],g[i-1]);break;case 20:break;case 21:this.$=[[g[i-2]].concat(g[i-1]),g[i]];break;case 22:this.$=[[g[i-1]].concat(g[i]),null];break;case 23:this.$=[[g[i-1]],g[i]];break;case 24:this.$=[[g[i]],null];break;case 25:g[i-1].push(g[i]),this.$=g[i-1];break;case 26:this.$=[g[i]];break;case 27:this.$=g[i];break;case 28:this.$=new e.StringNode(g[i]);break;case 29:this.$=new e.HashNode(g[i]);break;case 30:g[i-1].push(g[i]),this.$=g[i-1];break;case 31:this.$=[g[i]];break;case 32:this.$=[g[i-2],g[i]];break;case 33:this.$=[g[i-2],new e.StringNode(g[i])];break;case 34:this.$=new e.IdNode(g[i]);break;case 35:g[i-2].push(g[i]),this.$=g[i-2];break;case 36:this.$=[g[i]]}},table:[{3:1,4:2,5:[2,4],6:3,8:4,9:5,11:6,12:7,13:8,14:[1,9],15:[1,10],16:[1,12],19:[1,11],22:[1,13],23:[1,14],24:[1,15]},{1:[3]},{5:[1,16]},{5:[2,3],7:17,8:18,9:5,11:6,12:7,13:8,14:[1,9],15:[1,10],16:[1,12],19:[1,19],20:[2,3],22:[1,13],23:[1,14],24:[1,15]},{5:[2,5],14:[2,5],15:[2,5],16:[2,5],19:[2,5],20:[2,5],22:[2,5],23:[2,5],24:[2,5]},{4:20,6:3,8:4,9:5,11:6,12:7,13:8,14:[1,9],15:[1,10],16:[1,12],19:[1,11],20:[2,4],22:[1,13],23:[1,14],24:[1,15]},{4:21,6:3,8:4,9:5,11:6,12:7,13:8,14:[1,9],15:[1,10],16:[1,12],19:[1,11],20:[2,4],22:[1,13],23:[1,14],24:[1,15]},{5:[2,9],14:[2,9],15:[2,9],16:[2,9],19:[2,9],20:[2,9],22:[2,9],23:[2,9],24:[2,9]},{5:[2,10],14:[2,10],15:[2,10],16:[2,10],19:[2,10],20:[2,10],22:[2,10],23:[2,10],24:[2,10]},{5:[2,11],14:[2,11],15:[2,11],16:[2,11],19:[2,11],20:[2,11],22:[2,11],23:[2,11],24:[2,11]},{5:[2,12],14:[2,12],15:[2,12],16:[2,12],19:[2,12],20:[2,12],22:[2,12],23:[2,12],24:[2,12]},{17:22,21:23,31:[1,25],33:24},{17:26,21:23,31:[1,25],33:24},{17:27,21:23,31:[1,25],33:24},{17:28,21:23,31:[1,25],33:24},{21:29,31:[1,25],33:24},{1:[2,1]},{6:30,8:4,9:5,11:6,12:7,13:8,14:[1,9],15:[1,10],16:[1,12],19:[1,11],22:[1,13],23:[1,14],24:[1,15]},{5:[2,6],14:[2,6],15:[2,6],16:[2,6],19:[2,6],20:[2,6],22:[2,6],23:[2,6],24:[2,6]},{17:22,18:[1,31],21:23,31:[1,25],33:24},{10:32,20:[1,33]},{10:34,20:[1,33]},{18:[1,35]},{18:[2,24],21:40,25:36,26:37,27:38,28:[1,41],29:39,30:42,31:[1,43],33:24},{18:[2,34],28:[2,34],31:[2,34],34:[1,44]},{18:[2,36],28:[2,36],31:[2,36],34:[2,36]},{18:[1,45]},{18:[1,46]},{18:[1,47]},{18:[1,48],21:49,31:[1,25],33:24},{5:[2,2],8:18,9:5,11:6,12:7,13:8,14:[1,9],15:[1,10],16:[1,12],19:[1,11],20:[2,2],22:[1,13],23:[1,14],24:[1,15]},{14:[2,20],15:[2,20],16:[2,20],19:[2,20],22:[2,20],23:[2,20],24:[2,20]},{5:[2,7],14:[2,7],15:[2,7],16:[2,7],19:[2,7],20:[2,7],22:[2,7],23:[2,7],24:[2,7]},{21:50,31:[1,25],33:24},{5:[2,8],14:[2,8],15:[2,8],16:[2,8],19:[2,8],20:[2,8],22:[2,8],23:[2,8],24:[2,8]},{14:[2,14],15:[2,14],16:[2,14],19:[2,14],20:[2,14],22:[2,14],23:[2,14],24:[2,14]},{18:[2,22],21:40,26:51,27:52,28:[1,41],29:39,30:42,31:[1,43],33:24},{18:[2,23]},{18:[2,26],28:[2,26],31:[2,26]},{18:[2,29],30:53,31:[1,54]},{18:[2,27],28:[2,27],31:[2,27]},{18:[2,28],28:[2,28],31:[2,28]},{18:[2,31],31:[2,31]},{18:[2,36],28:[2,36],31:[2,36],32:[1,55],34:[2,36]},{31:[1,56]},{14:[2,13],15:[2,13],16:[2,13],19:[2,13],20:[2,13],22:[2,13],23:[2,13],24:[2,13]},{5:[2,16],14:[2,16],15:[2,16],16:[2,16],19:[2,16],20:[2,16],22:[2,16],23:[2,16],24:[2,16]},{5:[2,17],14:[2,17],15:[2,17],16:[2,17],19:[2,17],20:[2,17],22:[2,17],23:[2,17],24:[2,17]},{5:[2,18],14:[2,18],15:[2,18],16:[2,18],19:[2,18],20:[2,18],22:[2,18],23:[2,18],24:[2,18]},{18:[1,57]},{18:[1,58]},{18:[2,21]},{18:[2,25],28:[2,25],31:[2,25]},{18:[2,30],31:[2,30]},{32:[1,55]},{21:59,28:[1,60],31:[1,25],33:24},{18:[2,35],28:[2,35],31:[2,35],34:[2,35]},{5:[2,19],14:[2,19],15:[2,19],16:[2,19],19:[2,19],20:[2,19],22:[2,19],23:[2,19],24:[2,19]},{5:[2,15],14:[2,15],15:[2,15],16:[2,15],19:[2,15],20:[2,15],22:[2,15],23:[2,15],24:[2,15]},{18:[2,32],31:[2,32]},{18:[2,33],31:[2,33]}],defaultActions:{16:[2,1],37:[2,23],51:[2,21]},parseError:function(b,c){throw new Error(b)},parse:function(b){function p(){var a;a=c.lexer.lex()||1,typeof a!="number"&&(a=c.symbols_[a]||a);return a}function o(a){d.length=d.length-2*a,e.length=e.length-a,f.length=f.length-a}var c=this,d=[0],e=[null],f=[],g=this.table,h="",i=0,j=0,k=0,l=2,m=1;this.lexer.setInput(b),this.lexer.yy=this.yy,this.yy.lexer=this.lexer,typeof this.lexer.yylloc=="undefined"&&(this.lexer.yylloc={});var n=this.lexer.yylloc;f.push(n),typeof this.yy.parseError=="function"&&(this.parseError=this.yy.parseError);var q,r,s,t,u,v,w={},x,y,z,A;for(;;){s=d[d.length-1],this.defaultActions[s]?t=this.defaultActions[s]:(q==null&&(q=p()),t=g[s]&&g[s][q]);if(typeof t=="undefined"||!t.length||!t[0]){if(!k){A=[];for(x in g[s])this.terminals_[x]&&x>2&&A.push("'"+this.terminals_[x]+"'");var B="";this.lexer.showPosition?B="Parse error on line "+(i+1)+":\n"+this.lexer.showPosition()+"\nExpecting "+A.join(", "):B="Parse error on line "+(i+1)+": Unexpected "+(q==1?"end of input":"'"+(this.terminals_[q]||q)+"'"),this.parseError(B,{text:this.lexer.match,token:this.terminals_[q]||q,line:this.lexer.yylineno,loc:n,expected:A})}if(k==3){if(q==m)throw new Error(B||"Parsing halted.");j=this.lexer.yyleng,h=this.lexer.yytext,i=this.lexer.yylineno,n=this.lexer.yylloc,q=p()}for(;;){if(l.toString()in g[s])break;if(s==0)throw new Error(B||"Parsing halted.");o(1),s=d[d.length-1]}r=q,q=l,s=d[d.length-1],t=g[s]&&g[s][l],k=3}if(t[0]instanceof Array&&t.length>1)throw new Error("Parse Error: multiple actions possible at state: "+s+", token: "+q);switch(t[0]){case 1:d.push(q),e.push(this.lexer.yytext),f.push(this.lexer.yylloc),d.push(t[1]),q=null,r?(q=r,r=null):(j=this.lexer.yyleng,h=this.lexer.yytext,i=this.lexer.yylineno,n=this.lexer.yylloc,k>0&&k--);break;case 2:y=this.productions_[t[1]][1],w.$=e[e.length-y],w._$={first_line:f[f.length-(y||1)].first_line,last_line:f[f.length-1].last_line,first_column:f[f.length-(y||1)].first_column,last_column:f[f.length-1].last_column},v=this.performAction.call(w,h,j,i,this.yy,t[1],e,f);if(typeof v!="undefined")return v;y&&(d=d.slice(0,-1*y*2),e=e.slice(0,-1*y),f=f.slice(0,-1*y)),d.push(this.productions_[t[1]][0]),e.push(w.$),f.push(w._$),z=g[d[d.length-2]][d[d.length-1]],d.push(z);break;case 3:return!0}}return!0}},b=function(){var a={EOF:1,parseError:function(b,c){if(this.yy.parseError)this.yy.parseError(b,c);else throw new Error(b)},setInput:function(a){this._input=a,this._more=this._less=this.done=!1,this.yylineno=this.yyleng=0,this.yytext=this.matched=this.match="",this.conditionStack=["INITIAL"],this.yylloc={first_line:1,first_column:0,last_line:1,last_column:0};return this},input:function(){var a=this._input[0];this.yytext+=a,this.yyleng++,this.match+=a,this.matched+=a;var b=a.match(/\n/);b&&this.yylineno++,this._input=this._input.slice(1);return a},unput:function(a){this._input=a+this._input;return this},more:function(){this._more=!0;return this},pastInput:function(){var a=this.matched.substr(0,this.matched.length-this.match.length);return(a.length>20?"...":"")+a.substr(-20).replace(/\n/g,"")},upcomingInput:function(){var a=this.match;a.length<20&&(a+=this._input.substr(0,20-a.length));return(a.substr(0,20)+(a.length>20?"...":"")).replace(/\n/g,"")},showPosition:function(){var a=this.pastInput(),b=Array(a.length+1).join("-");return a+this.upcomingInput()+"\n"+b+"^"},next:function(){if(this.done)return this.EOF;this._input||(this.done=!0);var a,b,c,d;this._more||(this.yytext="",this.match="");var e=this._currentRules();for(var f=0;f<e.length;f++){b=this._input.match(this.rules[e[f]]);if(b){d=b[0].match(/\n.*/g),d&&(this.yylineno+=d.length),this.yylloc={first_line:this.yylloc.last_line,last_line:this.yylineno+1,first_column:this.yylloc.last_column,last_column:d?d[d.length-1].length-1:this.yylloc.last_column+b[0].length},this.yytext+=b[0],this.match+=b[0],this.matches=b,this.yyleng=this.yytext.length,this._more=!1,this._input=this._input.slice(b[0].length),this.matched+=b[0],a=this.performAction.call(this,this.yy,this,e[f],this.conditionStack[this.conditionStack.length-1]);if(a)return a;return}}if(this._input==="")return this.EOF;this.parseError("Lexical error on line "+(this.yylineno+1)+". Unrecognized text.\n"+this.showPosition(),{text:"",token:null,line:this.yylineno})},lex:function(){var b=this.next();return typeof b!="undefined"?b:this.lex()},begin:function(b){this.conditionStack.push(b)},popState:function(){return this.conditionStack.pop()},_currentRules:function(){return this.conditions[this.conditionStack[this.conditionStack.length-1]].rules}};a.performAction=function(b,c,d,e){var f=e;switch(d){case 0:this.begin("mu");if(c.yytext)return 14;break;case 1:return 14;case 2:return 24;case 3:return 16;case 4:return 20;case 5:return 19;case 6:return 19;case 7:return 23;case 8:return 23;case 9:c.yytext=c.yytext.substr(3,c.yyleng-5),this.begin("INITIAL");return 15;case 10:return 22;case 11:return 32;case 12:return 31;case 13:return 31;case 14:return 34;case 15:break;case 16:this.begin("INITIAL");return 18;case 17:this.begin("INITIAL");return 18;case 18:c.yytext=c.yytext.substr(1,c.yyleng-2).replace(/\\"/g,'"');return 28;case 19:return 31;case 20:return"INVALID";case 21:return 5}},a.rules=[/^[^\x00]*?(?=(\{\{))/,/^[^\x00]+/,/^\{\{>/,/^\{\{#/,/^\{\{\//,/^\{\{\^/,/^\{\{\s*else\b/,/^\{\{\{/,/^\{\{&/,/^\{\{![\s\S]*?\}\}/,/^\{\{/,/^=/,/^\.(?=[} ])/,/^\.\./,/^[/.]/,/^\s+/,/^\}\}\}/,/^\}\}/,/^"(\\["]|[^"])*"/,/^[a-zA-Z0-9_-]+(?=[=} /.])/,/^./,/^$/],a.conditions={mu:{rules:[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21],inclusive:!1},INITIAL:{rules:[0,1,21],inclusive:!0}};return a}();a.lexer=b;return a}();typeof require!="undefined"&&typeof exports!="undefined"&&(exports.parser=handlebars,exports.parse=function(){return handlebars.parse.apply(handlebars,arguments)},exports.main=function(b){if(!b[1])throw new Error("Usage: "+b[0]+" FILE");if(typeof process!="undefined")var c=require("fs").readFileSync(require("path").join(process.cwd(),b[1]),"utf8");else var d=require("file").path(require("file").cwd()),c=d.join(b[1]).read({charset:"utf-8"});return exports.parser.parse(c)},typeof module!="undefined"&&require.main===module&&exports.main(typeof process!="undefined"?process.argv.slice(1):require("system").args));var Handlebars={};Handlebars.VERSION="1.0.beta.1",Handlebars.Parser=handlebars,Handlebars.parse=function(a){Handlebars.Parser.yy=Handlebars.AST;return Handlebars.Parser.parse(a)},Handlebars.print=function(a){return(new Handlebars.PrintVisitor).accept(a)},Handlebars.helpers={},Handlebars.partials={},Handlebars.registerHelper=function(a,b,c){c&&(b.not=c),this.helpers[a]=b},Handlebars.registerPartial=function(a,b){this.partials[a]=b},Handlebars.registerHelper("helperMissing",function(a){if(arguments.length===2)return undefined;throw new Error("Could not find property '"+a+"'")}),Handlebars.registerHelper("blockHelperMissing",function(a,b,c){c=c||function(){};var d="",e=Object.prototype.toString.call(a);e==="[object Function]"&&(a=a());if(a===!0)return b(this);if(a===!1||a==null)return c(this);if(e==="[object Array]"){if(a.length>0)for(var f=0,g=a.length;f<g;f++)d=d+b(a[f]);else d=c(this);return d}return b(a)},function(a,b){return b(a)}),Handlebars.registerHelper("each",function(a,b,c){var d="";if(a&&a.length>0)for(var e=0,f=a.length;e<f;e++)d=d+b(a[e]);else d=c(this);return d}),Handlebars.registerHelper("if",function(a,b,c){return!a||a==[]?c(this):b(this)}),Handlebars.registerHelper("unless",function(a,b,c){return Handlebars.helpers["if"].call(this,a,c,b)}),Handlebars.registerHelper("with",function(a,b){return b(a)}),Handlebars.logger={DEBUG:0,INFO:1,WARN:2,ERROR:3,level:3,log:function(a,b){}},Handlebars.log=function(a,b){Handlebars.logger.log(a,b)},function(){Handlebars.AST={},Handlebars.AST.ProgramNode=function(a,b){this.type="program",this.statements=a,b&&(this.inverse=new Handlebars.AST.ProgramNode(b))},Handlebars.AST.MustacheNode=function(a,b,c){this.type="mustache",this.id=a[0],this.params=a.slice(1),this.hash=b,this.escaped=!c},Handlebars.AST.PartialNode=function(a,b){this.type="partial",this.id=a,this.context=b};var a=function(a,b){if(a.original!==b.original)throw new Handlebars.Exception(a.original+" doesn't match "+b.original)};Handlebars.AST.BlockNode=function(b,c,d){a(b.id,d),this.type="block",this.mustache=b,this.program=c},Handlebars.AST.InverseNode=function(b,c,d){a(b.id,d),this.type="inverse",this.mustache=b,this.program=c},Handlebars.AST.ContentNode=function(a){this.type="content",this.string=a},Handlebars.AST.HashNode=function(a){this.type="hash",this.pairs=a},Handlebars.AST.IdNode=function(a){this.type="ID",this.original=a.join(".");var b=[],c=0;for(var d=0,e=a.length;d<e;d++){var f=a[d];if(f==="..")c++;else{if(f==="."||f==="this")continue;b.push(f)}}this.parts=b,this.string=b.join("."),this.depth=c,this.isSimple=b.length===1&&c===0},Handlebars.AST.StringNode=function(a){this.type="STRING",this.string=a},Handlebars.AST.CommentNode=function(a){this.type="comment",this.comment=a}}(),Handlebars.Visitor=function(){},Handlebars.Visitor.prototype={accept:function(a){return this[a.type](a)}},Handlebars.Exception=function(a){this.message=a},Handlebars.SafeString=function(a){this.string=a},Handlebars.SafeString.prototype.toString=function(){return this.string.toString()},function(){var a={"<":"&lt;",">":"&gt;"},b=/&(?!\w+;)|[<>]/g,c=/[&<>]/,d=function(b){return a[b]||"&amp;"};Handlebars.Utils={escapeExpression:function(a){if(a instanceof Handlebars.SafeString)return a.toString();if(a==null||a===!1)return"";if(!c.test(a))return a;return a.replace(b,d)},isEmpty:function(a){return typeof a=="undefined"?!0:a===null?!0:a===!1?!0:Object.prototype.toString.call(a)==="[object Array]"&&a.length===0?!0:!1}}}(),Handlebars.Compiler=function(){},Handlebars.JavaScriptCompiler=function(){},function(a,b){a.OPCODE_MAP={appendContent:1,getContext:2,lookupWithHelpers:3,lookup:4,append:5,invokeMustache:6,appendEscaped:7,pushString:8,truthyOrFallback:9,functionOrFallback:10,invokeProgram:11,invokePartial:12,push:13,invokeInverse:14,assignToHash:15,pushStringParam:16},a.MULTI_PARAM_OPCODES={appendContent:1,getContext:1,lookupWithHelpers:1,lookup:1,invokeMustache:2,pushString:1,truthyOrFallback:1,functionOrFallback:1,invokeProgram:2,invokePartial:1,push:1,invokeInverse:1,assignToHash:1,pushStringParam:1},a.DISASSEMBLE_MAP={};for(var c in a.OPCODE_MAP){var d=a.OPCODE_MAP[c];a.DISASSEMBLE_MAP[d]=c}a.multiParamSize=function(b){return a.MULTI_PARAM_OPCODES[a.DISASSEMBLE_MAP[b]]},a.prototype={compiler:a,disassemble:function(){var b=this.opcodes,c,d,e=[],f,g,h;for(var i=0,j=b.length;i<j;i++){c=b[i];if(c==="DECLARE")g=b[++i],h=b[++i],e.push("DECLARE "+g+" = "+h);else{f=a.DISASSEMBLE_MAP[c];var k=a.multiParamSize(c),l=[];for(var m=0;m<k;m++)d=b[++i],typeof d=="string"&&(d='"'+d.replace("\n","\\n")+'"'),l.push(d);f=f+" "+l.join(" "),e.push(f)}}return e.join("\n")},guid:0,compile:function(a,b){this.children=[],this.depths={list:[]},this.options=b||{};return this.program(a)},accept:function(a){return this[a.type](a)},program:function(a){var b=a.statements,c;this.opcodes=[];for(var d=0,e=b.length;d<e;d++)c=b[d],this[c.type](c);this.depths.list=this.depths.list.sort(function(a,b){return a-b});return this},compileProgram:function(a){var b=(new this.compiler).compile(a,this.options),c=this.guid++;this.usePartial=this.usePartial||b.usePartial,this.children[c]=b;for(var d=0,e=b.depths.list.length;d<e;d++){depth=b.depths.list[d];if(depth<2)continue;this.addDepth(depth-1)}return c},block:function(a){var b=a.mustache,c,d,e,f,g=this.setupStackForMustache(b),h=this.compileProgram(a.program);a.program.inverse&&(f=this.compileProgram(a.program.inverse),this.declare("inverse",f)),this.opcode("invokeProgram",h,g.length),this.declare("inverse",null),this.opcode("append")},inverse:function(a){this.ID(a.mustache.id);var b=this.compileProgram(a.program);this.opcode("invokeInverse",b),this.opcode("append")},hash:function(a){var b=a.pairs,c,d;this.opcode("push","{}");for(var e=0,f=b.length;e<f;e++)c=b[e],d=c[1],this.accept(d),this.opcode("assignToHash",c[0])},partial:function(a){var b=a.id;this.usePartial=!0,a.context?this.ID(a.context):this.opcode("push","context"),this.opcode("invokePartial",b.original),this.opcode("append")},content:function(a){this.opcode("appendContent",a.string)},mustache:function(a){var b=this.setupStackForMustache(a);this.opcode("invokeMustache",b.length,a.id.original),a.escaped?this.opcode("appendEscaped"):this.opcode("append")},ID:function(a){this.addDepth(a.depth),this.opcode("getContext",a.depth),this.opcode("lookupWithHelpers",a.parts[0]||null);for(var b=1,c=a.parts.length;b<c;b++)this.opcode("lookup",a.parts[b])},STRING:function(a){this.opcode("pushString",a.string)},comment:function(){},pushParams:function(a){var b=a.length,c;while(b--)c=a[b],this.options.stringParams?(c.depth&&this.addDepth(c.depth),this.opcode("getContext",c.depth||0),this.opcode("pushStringParam",c.string)):this[c.type](c)},opcode:function(b,c,d){this.opcodes.push(a.OPCODE_MAP[b]),c!==undefined&&this.opcodes.push(c),d!==undefined&&this.opcodes.push(d)},declare:function(a,b){this.opcodes.push("DECLARE"),this.opcodes.push(a),this.opcodes.push(b)},addDepth:function(a){a!==0&&(this.depths[a]||(this.depths[a]=!0,this.depths.list.push(a)))},setupStackForMustache:function(a){var b=a.params;this.pushParams(b),a.hash?this.hash(a.hash):this.opcode("push","{}"),this.ID(a.id);return b}},b.prototype={nameLookup:function(a,c,d){return b.RESERVED_WORDS[c]||c.indexOf("-")!==-1?a+"['"+c+"']":a+"."+c},appendToBuffer:function(a){return"buffer = buffer + "+a+";"},initializeBuffer:function(){return this.quotedString("")},compile:function(a,b){this.environment=a,this.options=b||{},this.preamble(),this.stackSlot=0,this.stackVars=[],this.registers={list:[]},this.compileChildren(a,b),Handlebars.log(Handlebars.logger.DEBUG,a.disassemble()+"\n\n");var c=a.opcodes,d,e,f,h;this.i=0;for(g=c.length;this.i<g;this.i++)d=this.nextOpcode(0),d[0]==="DECLARE"?(this.i=this.i+2,this[d[1]]=d[2]):(this.i=this.i+d[1].length,this[d[0]].apply(this,d[1]));return this.createFunction()},nextOpcode:function(b){var c=this.environment.opcodes,d=c[this.i+b],e,f,g,h;if(d==="DECLARE"){e=c[this.i+1],f=c[this.i+2];return["DECLARE",e,f]}e=a.DISASSEMBLE_MAP[d],g=a.multiParamSize(d),h=[];for(var i=0;i<g;i++)h.push(c[this.i+i+1+b]);return[e,h]},eat:function(a){this.i=this.i+a.length},preamble:function(){var a=[];a.push("var buffer = "+this.initializeBuffer()+", currentContext = context");var b="helpers = helpers || Handlebars.helpers;";this.environment.usePartial&&(b=b+" partials = partials || Handlebars.partials;"),a.push(b),this.lastContext=0,this.source=a},createFunction:function(){var a={escapeExpression:Handlebars.Utils.escapeExpression,invokePartial:Handlebars.VM.invokePartial,programs:[],program:function(a,b,c,d){var e=this.programs[a];if(d)return Handlebars.VM.program(this.children[a],b,c,d);if(e)return e;e=this.programs[a]=Handlebars.VM.program(this.children[a],b,c);return e},programWithDepth:Handlebars.VM.programWithDepth,noop:Handlebars.VM.noop},b=this.stackVars.concat(this.registers.list);b.length>0&&(this.source[0]=this.source[0]+", "+b.join(", ")),this.source[0]=this.source[0]+";",this.source.push("return buffer;");var c=["Handlebars","context","helpers","partials"];this.options.data&&c.push("data");for(var d=0,e=this.environment.depths.list.length;d<e;d++)c.push("depth"+this.environment.depths.list[d]);c.length===4&&!this.environment.usePartial&&c.pop(),c.push(this.source.join("\n"));var f=Function.apply(this,c);f.displayName="Handlebars.js",Handlebars.log(Handlebars.logger.DEBUG,f.toString()+"\n\n"),a.render=f,a.children=this.environment.children;return function(b,c,d){try{c=c||{};var e=[Handlebars,b,c.helpers,c.partials,c.data],f=Array.prototype.slice.call(arguments,2);e=e.concat(f);return a.render.apply(a,e)}catch(g){throw g}}},appendContent:function(a){this.source.push(this.appendToBuffer(this.quotedString(a)))},append:function(){var a=this.popStack();this.source.push("if("+a+" || "+a+" === 0) { "+this.appendToBuffer(a)+" }")},appendEscaped:function(){var a=this.nextOpcode(1),b="";a[0]==="appendContent"&&(b=" + "+this.quotedString(a[1][0]),this.eat(a)),this.source.push(this.appendToBuffer("this.escapeExpression("+this.popStack()+")"+b))},getContext:function(a){this.lastContext!==a&&(this.lastContext=a,a===0?this.source.push("currentContext = context;"):this.source.push("currentContext = depth"+a+";"))},lookupWithHelpers:function(a){if(a){var b=this.nextStack(),c="if('"+a+"' in helpers) { "+b+" = "+this.nameLookup("helpers",a,"helper")+"; } else { "+b+" = "+this.nameLookup("currentContext",a,"context")+"; }";this.source.push(c)}else this.pushStack("currentContext")},lookup:function(a){var b=this.topStack();this.source.push(b+" = "+this.nameLookup(b,a,"context")+";")},pushStringParam:function(a){this.pushStack("currentContext"),this.pushString(a)},pushString:function(a){this.pushStack(this.quotedString(a))},push:function(a){this.pushStack(a)},invokeMustache:function(a,b){this.populateParams(a,this.quotedString(b),"{}",null,function(a,b,c){this.source.push("else if("+c+"=== undefined) { "+a+" = helpers.helperMissing.call("+b+"); }"),this.source.push("else { "+a+" = "+c+"; }")})},invokeProgram:function(a,b){var c=this.programExpression(this.inverse),d=this.programExpression(a);this.populateParams(b,null,d,c,function(a,b,c){this.source.push("else { "+a+" = helpers.blockHelperMissing.call("+b+"); }")})},populateParams:function(a,b,c,d,e){var f=this.popStack(),g,h=[],i,j,k=this.popStack();this.register("tmp1",c),this.source.push("tmp1.hash = "+k+";"),this.options.stringParams&&this.source.push("tmp1.contexts = [];");for(var l=0;l<a;l++)i=this.popStack(),h.push(i),this.options.stringParams&&this.source.push("tmp1.contexts.push("+this.popStack()+");");d&&(this.source.push("tmp1.fn = tmp1;"),this.source.push("tmp1.inverse = "+d+";")),this.options.data&&this.source.push("tmp1.data = data;"),h.push("tmp1"),d&&h.push(d),this.populateCall(h,f,b||f,e)},populateCall:function(a,b,c,d){var e=["context"].concat(a).join(", "),f=["context"].concat(c).concat(a).join(", ");nextStack=this.nextStack(),this.source.push("if(typeof "+b+" === 'function') { "+nextStack+" = "+b+".call("+e+"); }"),d.call(this,nextStack,f,b)},invokeInverse:function(a){var b=this.programExpression(a),c=["context",this.topStack(),"this.noop",b];this.pushStack("helpers.blockHelperMissing.call("+c.join(", ")+")")},invokePartial:function(a){this.pushStack("this.invokePartial("+this.nameLookup("partials",a,"partial")+", '"+a+"', "+this.popStack()+", helpers, partials);")},assignToHash:function(a){var b=this.popStack(),c=this.topStack();this.source.push(c+"['"+a+"'] = "+b+";")},compiler:b,compileChildren:function(a,b){var c=a.children,d,e,f=[];for(var g=0,h=c.length;g<h;g++)d=c[g],e=new this.compiler,f[g]=e.compile(d,b);a.rawChildren=c,a.children=f},programExpression:function(a){if(a==null)return"this.noop";var b=[a,"helpers","partials"],c=this.environment.rawChildren[a].depths.list;this.options.data&&b.push("data");for(var d=0,e=c.length;d<e;d++)depth=c[d],depth===1?b.push("context"):b.push("depth"+(depth-1));this.environment.usePartial||(b[3]?b[2]="null":b.pop());if(c.length===0)return"this.program("+b.join(", ")+")";b[0]="this.children["+a+"]";return"this.programWithDepth("+b.join(", ")+")"},register:function(a,b){this.useRegister(a),this.source.push(a+" = "+b+";")},useRegister:function(a){this.registers[a]||(this.registers[a]=!0,this.registers.list.push(a))},pushStack:function(a){this.source.push(this.nextStack()+" = "+a+";");return"stack"+this.stackSlot},nextStack:function(){this.stackSlot++,this.stackSlot>this.stackVars.length&&this.stackVars.push("stack"+this.stackSlot);return"stack"+this.stackSlot},popStack:function(){return"stack"+this.stackSlot--},topStack:function(){return"stack"+this.stackSlot},quotedString:function(a){return'"'+a.replace(/\\/g,"\\\\").replace(/"/g,'\\"').replace(/\n/g,"\\n").replace(/\r/g,"\\r")+'"'}};var e="break case catch continue default delete do else finally for function if in instanceof new return switch this throw try typeof var void while with null true false".split(" ");compilerWords=b.RESERVED_WORDS={};for(var f=0,g=e.length;f<g;f++)compilerWords[e[f]]=!0}(Handlebars.Compiler,Handlebars.JavaScriptCompiler),Handlebars.VM={programWithDepth:function(a,b,c,d,e){var f=Array.prototype.slice.call(arguments,4);return function(e,g){g=g||{},g={helpers:g.helpers||b,partials:g.partials||c,data:g.data||d};return a.apply(this,[e,g].concat(f))}},program:function(a,b,c,d){return function(e,f){f=f||{};return a(e,{helpers:f.helpers||b,partials:f.partials||c,data:f.data||d})}},noop:function(){return""},compile:function(a,b){var c=Handlebars.parse(a),d=(new Handlebars.Compiler).compile(c,b);return(new Handlebars.JavaScriptCompiler).compile(d,b)},invokePartial:function(a,b,c,d,e){if(a===undefined)throw new Handlebars.Exception("The partial "+b+" could not be found");if(a instanceof Function)return a(c,{helpers:d,partials:e});e[b]=Handlebars.VM.compile(a);return e[b](c,{helpers:d,partials:e})}},Handlebars.compile=Handlebars.VM.compile