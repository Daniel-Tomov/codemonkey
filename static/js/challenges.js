var responseClass = document.getElementsByClassName("responses");
var completionStatus = document.getElementsByClassName("completionStatus");
var listOfButtons = document.getElementsByClassName('submitButtons');
var responseArray = [];
var completionButton = document.getElementById("completionButton");
var textAreas = document.getElementsByClassName("textAreaBox");
var codeMirrors = [];
var ctrlPressed = false;
$(document).keydown(function(event) {
  let activeElement = document.activeElement;
  if (activeElement.tagName != "TEXTAREA"){
    return;
  }
  activeElement = activeElement.parentElement.parentElement.parentElement
  if (event.keyCode == 9) {  //tab pressed
    event.preventDefault(); // stops its action
    //console.log(activeElement);
    //insertAtCursor(activeElement.id, "    ");
  }
  
  if (event.keyCode == 13 && ctrlPressed){
    event.preventDefault();
    ctrlPressed = false;
    submitChallenge(activeElement.id.replace("textarea", ""));
  }
  if (event.keyCode == 17){
    if (ctrlPressed == false){
      ctrlPressed = true;
    }
    else{
      ctrlPressed = false;
    }
  } else {
    ctrlPressed = false;
  }
});
function submitChallenge(clicked_id){
  var id = clicked_id.replace("submitButton", "");
  var ids = id.split("_");
  var destination = ids[2] + "response";
  document.getElementById(destination).innerHTML = "Running your code...";
  var chal_id = ids[0] + " " + ids[1] + " " + ids[2]
  let currentID = "";
  for (let i = 0; i < textAreas.length; i++){
    currentID = textAreas[i].id;
    if (currentID.includes(id)) {
      var the_code = codeMirrors[i].getValue();
      //var the_code = document.getElementById(id + "textarea").lastElementChild.getValue;
    }
  }

  runit(the_code, destination);
  output = document.getElementById(destination).innerHTML;
  //console.log(output);
  
  $.ajax({
    url: "/recieve_data",
    type: "get",
    data: {code: btoa(the_code), output: btoa(output), chal_id:btoa(chal_id)},
    success: function(response) {
      var resp = atob(response);
      document.getElementById(destination).innerHTML = resp + output;
      checkChallenges();
    },
    error: function(xhr) {
      //Do Something to handle error
    }
  });
}
  
function checkChallenges(){
  for (let i=0; i<responseClass.length; i++){
    if(responseClass[i].innerText.includes("Incorrect!")){
        completionStatus[i].innerText = "Incomplete";
        completionStatus[i].style.background = "red";
        responseArray[i] = "0";
      } else if(responseClass[i].innerText.includes("Error")){
        completionStatus[i].innerText = "Incomplete";
        completionStatus[i].style.background = "red";
        responseArray[i] = "0";
      } else if (responseClass[i].innerText.includes("Correct!")){
        responseArray[i] = "1";
        completionStatus[i].innerText = "Completed";
        completionStatus[i].style.background = "green";
      } else if(completionStatus[i].innerText.includes("Incomplete")){
        responseArray[i] = "0";
      }  else if(completionStatus[i].innerText.includes("Completed")) {
        responseArray[i] = "1";
      }
    }
    var counter = 0;
    for (let i=0; i<responseArray.length; i++){
      if (responseArray[i].includes("1")){
        counter++;
      }
    }
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
function getCookie(cname) {
  let name = cname + "=";
  let ca = document.cookie.split(';');
  for(let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}
function insertAtCursor(myFieldName, myValue) {
  for (let i = 0; i < textAreas.length; i++){
    currentID = textAreas[i].id;
    if (currentID.includes(id)) {
      codeMirrors[i].replaceSelection(myValue);
      //var the_code = document.getElementById(id + "textarea").lastElementChild.getValue;
    }
  }
  var myField = document.getElementById(myFieldName);
  //IE support
  if (document.selection) {
      myField.focus();
      sel = document.selection.createRange();
      sel.text = myValue;
  }
  //MOZILLA and others
  else if (myField.selectionStart || myField.selectionStart == '0') {
      var startPos = myField.selectionStart;
      var endPos = myField.selectionEnd;
      myField.value = myField.value.substring(0, startPos) + myValue + myField.value.substring(endPos, myField.value.length);
  } else {
      myField.value += myValue;
  }
}
let texts = document.getElementsByClassName("text");
for (let i = 0; i < texts.length; i++){
  var text = texts[i].innerText.toString();
  texts[i].innerHTML = text.replace(/\^lb\^/g, "<br>");
}
checkChallenges();
completionButton.addEventListener("click", function() {
  checkChallenges();
});
// Code mirror
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