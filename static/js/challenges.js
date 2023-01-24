var responseClass = document.getElementsByClassName("responses");
var completionStatus = document.getElementsByClassName("completionStatus");
var listOfButtons = document.getElementsByClassName('submitButtons');
var responseArray = [];
var completionButton = document.getElementById("completionButton");
var textAreas = document.getElementsByClassName("textAreaBox");
var codeMirrors = [];
var ctrlPressed = false;
var codeblocks = document.getElementsByClassName("codeblocks");


$(document).keydown(function(event) {
  let activeElement = document.activeElement;
  if (activeElement.tagName != "TEXTAREA"){
    return;
  }
  activeElement = activeElement.parentElement.parentElement.parentElement

  if (event.keyCode == 9) {  //tab pressed
    event.preventDefault(); // stops its action
  }
  // enter key is pressed     ctrl key was recently pressed  
  if (event.keyCode == 13 && ctrlPressed){
    event.preventDefault();
    ctrlPressed = false;
    // run codeblock code
    if (activeElement.id.includes("codeblock")){
      runCodeblock(activeElement.id);
    } else {
      //run question code
      submitChallenge(activeElement.id.replace("textarea", ""));
    }
  }
  // track if ctrl key was pressed
  if (event.keyCode == 17){
    if (ctrlPressed == false){
      ctrlPressed = true;
    }
    else{
      ctrlPressed = false;
    }
  } else {
    // every key press makes this false
    ctrlPressed = false;
  }
});

function runCodeblock(clicked_id){
  var id = clicked_id.replace("submitButton", "");
  // the div the text should go
  var destination = id + "response";
  document.getElementById(destination).innerHTML = "Running your code...";
  // go through all of the textareas on the page
  for (let i = 0; i < textAreas.length; i++){
    if (textAreas[i].id.replace("", "") == id) {
      var the_code = codeMirrors[i].getValue();
      runit(the_code, (destination));
    }
  }

}

async function submitChallenge(clicked_id){
  var id = clicked_id.replace("submitButton", "");
  // the id has underscores in it
  var ids = id.split("_");
  var destination = ids[2] + "response";
  document.getElementById(destination).innerHTML = "Running your code...";
  var chal_id = ids[0] + " " + ids[1] + " " + ids[2];
  for (let i = 0; i < textAreas.length; i++){
    // if the id of the current index of the textAreas array is equal to the id we are looking for
    if (textAreas[i].id.replace("textarea", "") == id) {
      // then get the codeMirror object correspodning to that textarea.
      var the_code = codeMirrors[i].getValue();
      // evaluate code with Skulpt
      await runit(the_code, (destination + "_output"));
    }
  }

  output = document.getElementById(destination + "_output").innerHTML;

  // send the user's code and evaluated output to the server for completion validation
  $.ajax({
    url: "/recieve_data",
    type: "get",
    data: {code: btoa(the_code), output: btoa(output), chal_id:btoa(chal_id)},
    success: function(response) {
      // set the response div to equal the response from the server
      document.getElementById(destination).innerHTML = atob(response);
      // check the whole page for completeness
      checkChallenges();
    },
    error: function(xhr) {
      document.getElementById(destination).innerHTML = "There has been an error sending your code to the server. Please try again later.";
    }
  });
}
  
function checkChallenges(){
  // go through all of the response divs and see if they are correct or not
  var counter = 0
  for (let i=0; i<responseClass.length; i++){

    // responseClass is the completion indicator below the textarea
    if(responseClass[i].innerText.includes("Incorrect!")){
        completionStatus[i].innerText = "Incomplete";
        completionStatus[i].style.background = "red";

      } else if(responseClass[i].innerText.includes("Error")){
        completionStatus[i].innerText = "Incomplete";
        completionStatus[i].style.background = "red";
      
      } else if (responseClass[i].innerText.includes("Correct!")){
        counter++;
        completionStatus[i].innerText = "Completed";
        completionStatus[i].style.background = "green";
      
        // completionStatus is the completion indicator above the textarea
      } else if(completionStatus[i].innerText.includes("Incomplete")){
        responseArray[i] = "0";
      
      }  else if(completionStatus[i].innerText.includes("Completed")) {
        counter++;
      }
    }
    // if the counter is equal to the responseClass length, then the user has completed the module
    if (counter == responseClass.length){
      completionButton.innerText = "Completed";
      completionButton.style.background = "green";
      var value = completionButton.value.split("_");
      completionButton.value = value[0] + "_complete"
    } else{
      completionButton.innerText = "Uncompleted";
      completionButton.style.background = "red";
      var value = completionButton.value.split("_");
      completionButton.value = value[0] + "_uncomplete"
    }
    // notify the server of the user's course completion status
    var page_id = completionButton.value.split("_")[0];
    var status = completionButton.value.split("_")[1];
    $.ajax({
        url: "/completions",
        type: "get",
        data: {page_id:btoa(page_id), status:btoa(status)},
      error: function(xhr) {
        //Do Something to handle error
      }
    });
}

let texts = document.getElementsByClassName("text");
for (let i = 0; i < texts.length; i++){
  var text = texts[i].innerText.toString();
  texts[i].innerHTML = text.replace(/\^lb\^/g, "<br>");
}

checkChallenges();

// Create Code Mirror instances
for (let i = 0; i < textAreas.length; i++){
  var editor = CodeMirror.fromTextArea(textAreas[i].firstElementChild, {
    lineNumbers: true,
    mode: {
      name: "python",
      version: 3,
      singleLineStringErrors: false
    },
    matchBrackets: true,
    extraKeys: {
      //Tab: false,
      "Enter": false,
      "Ctrl": false,
    }
  });
  codeMirrors.push(editor);
} 