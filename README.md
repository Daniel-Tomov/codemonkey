# Code Monkey

For me and other people in my group: 
<ul>
  <li>Submission Form: <a href="https://docs.google.com/forms/d/e/1FAIpQLSeWqrl5Fv2bUUb8hKgddbWtL_wgjdhOrIMJ5EPcReuUGyQniA/viewform"> Google Pre-Proposal Form</a></li>
  <li>Shared Document: <a href="https://docs.google.com/document/d/1VxrSXIrScJ1PQG0PVCgcN-ZDyvmENHpNuVRCk0shqvc/edit">Google Document</a></li>
</ul>

## To Do List

### General
:white_check_mark: Create domain with SSL (codemonkey.tk)

:x: Submit code from front end to back end without refreshing the page. Also send the backend information to the front end without refreshing the page. This will mostly be used for submitting code to the server to run and check against the reqirements.

:white_check_mark: Use session tokens stored in a cookie to authenticate users

### Front End

:white_check_mark: Create admin page

:x: Make admin page look pretty

:white_check_mark: Create login page

:x: Make login page pretty

:white_check_mark: Create default page

:x: Make default page look pretty

:x: Create register page

:x: Make register page look pretty

:x: Create a function to submit code to the backend

:x: Receive code execution details from the backend

### Backend

:white_check_mark: Use tokens to authenticate users
<ul>
  <li>Should have an expiration date</li>
  <li>Should refresh every time a user reloads a page</li>
</ul>

:x: Use json for formating data

:white_check_mark: Put the session token into a cookie instead of plainly in the HTML. Also means the cookie has to be accessed by the backend.

:x: Track course completion for each user

:x: Store user information in a database instead of a text file

:white_check_mark: Use threading to remove inactive sessions every minute.

:x: Accept code submit requests from the frontend

:x: Execute code from the frontend

:x: Send code back to the frontend

## Functionality of Pages

### Login
<ol>
  <li>User enters login credentials</li>
  <li>Backend hashes the password five times, creates a session token, and an expiration date for the token.</li>
  <li>Token (and only the token) is sent back to the front end to be part of the front-end HTML through a cookie</li>
  <li>The user is sent to the challenges page</li>
</ol>

### Loading a Normal Webpage 
<ol>
  <li>Session token, and any other information is sent to back end</li>
  <li>Backend checks if token is expired. Yes -> log the user out. No -> Continue</li>
  <li>Determine the next page that needs to be loaded.</li>
  <li>Send information about the next page to the front end or redirect the user to the correct page</li>
</ol>
