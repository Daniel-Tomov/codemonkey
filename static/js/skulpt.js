// Skulpt example code from the skulpt.org website

function outf(text) {
    var mypre = document.getElementById(Sk.pre);
    mypre.innerText = mypre.innerText + text + "";

}

function builtinRead(x) {
    if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
            throw "File not found: '" + x + "'";
    return Sk.builtinFiles["files"][x];
}

function runit(theCode, destination) { 
   var prog = theCode; 
   var mypre = document.getElementById(destination); 
   mypre.innerHTML = ''; 
   Sk.pre = destination;
   Sk.configure({
    output:outf,
    read:builtinRead,
    __future__: Sk.python3
    }); 
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