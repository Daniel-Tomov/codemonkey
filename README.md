# Code Monkey

For me and other people in my group: 
<ul>
  <li>Submission Form: https://docs.google.com/forms/d/e/1FAIpQLSeWqrl5Fv2bUUb8hKgddbWtL_wgjdhOrIMJ5EPcReuUGyQniA/viewform</li>
  <li>Shared Document: https://docs.google.com/document/d/1VxrSXIrScJ1PQG0PVCgcN-ZDyvmENHpNuVRCk0shqvc/edit</li>
</ul>


### General
:white_check_mark: Create domain with SSL (codemonkey.tk)

:x: Submit code from front end to back end without refreshing the page. Also send the backend information to the front end without refreshing the page.

### Front End

:white_check_mark: Create admin page

:x: Make admin page look pretty

:white_check_mark: Create login page

:x: Make login page pretty

:x: Create default page

### Backend

:x: Use tokens to authenticate users
<ul>
  <li>Should have an expiration date</li>
  <li>Should be kept in a json string</li>
  <li>Should refresh every time a user reloads a page</li>
</ul>

:x: Use json for formating data

:x: Put the session token into a cookie instead of plainly in the HTML. Also means the cookie has to be accessed by the backend.

:x: Track course completion for each user

:x: Store user information in a database instead of a text file

:x: Use threading to remove inactive sessions every minute.

:white_check_mark: Fix the #TODO in sessions.py

## Expected Functionality of Pages

### Login
<ol>
  <li>User enters login credentials</li>
  <li>Backend hashes password with the password as the key, creates a session token, and an expiration date for the token.</li>
  <li>Token (and only the token) is sent back to the front end to be part of the front-end HTML</li>
</ol>

### Loading a Normal Webpage 
<ol>
  <li>Session token, and any other information is sent to back end</li>
  <li>Backend checks if token is expired. Yes -> log the user out. No -> Continue</li>
  <li>Determine the next page that needs to be loaded.</li>
  <li>Send information about the next page to the front end or redirect the user to the correct page</li>
</ol>


## Todo

:x: Fix printing token in login function

:x: Fix printing of post request information in login function