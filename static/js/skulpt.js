// output functions are configurable.  This one just appends some text
// to a pre element.
function outf(text) {
    var mypre = document.getElementById(Sk.pre);
    mypre.innerHTML = mypre.innerHTML + text + "<br>";
    mypre.innerHTML = mypre.innerHTML.replace(/<br>\n<br>/g, "<br>");
}

function builtinRead(x) {
    if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
            throw "File not found: '" + x + "'";
    return Sk.builtinFiles["files"][x];
}

// Here's everything you need to run a python program in skulpt
// grab the code from your textarea
// get a reference to your pre element for output
// configure the output function
// call Sk.importMainWithBody()
function runit(theCode, destination) { 
   var prog = theCode; 
   var mypre = document.getElementById(destination); 
   mypre.innerHTML = ''; 
   Sk.pre = destination;
   Sk.configure({output:outf, read:builtinRead}); 
   //alert(prog);
   var myPromise = Sk.misceval.asyncToPromise(function() {
       return Sk.importMainWithBody("<stdin>", false, prog, true);
   });

   myPromise.then(function(mod) {
       console.log('success');
   },
       function(err) {
       document.getElementById(destination).innerHTML = document.getElementById(destination).innerHTML + err.toString();
   });
}