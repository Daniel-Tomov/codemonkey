# Code Monkey

Code Monkey is an online program that provides introduction to programming courses. It was created for my Senior Project at Landstown High School. The project had to be related to the strand I was enrolled in: Cybersecurity.

Read the latest One Pager <a href="documents/Proposal Draft 2.pdf">here</a>

## To Do List

### General
:white_check_mark: Create domain with SSL (codemonkey.tk)

:white_check_mark: Submit code from front end to back end without refreshing the page. Also send the backend information to the front end without refreshing the page. This will mostly be used for submitting code to the server to run and check against the reqirements.

:white_check_mark: Use session tokens stored in a cookie to authenticate users

### Front End

:white_check_mark: Create admin page

:x: Make admin page look pretty

:white_check_mark: Create login page

:x: Make login page pretty

:white_check_mark: Create default page

:x: Make default page look pretty

:x: Create register page

:x: Add emails to register page

:x: Make register page look pretty

:x: Create a function to submit code to the backend

:x: Receive code execution details from the backend

:x: Create a page that recieves challenges and displays them to the user.

:x: Make page for each challenge look pretty

:x: Password restrictions for weak passwords

### Backend

:white_check_mark: Use tokens to authenticate users. These tokens should:
<ul>
  <li>Should have an expiration date</li>
  <li>Should refresh every time a user reloads a page</li>
</ul>

:white_check_mark: Use dictionaries and classes/objects for storing data

:white_check_mark: Put the session token into a cookie instead of plainly in the HTML. The cookie also has to be accessed by the backend.

:white_check_mark: Track course completion for each user

:white_check_mark: Course completion should also be in a database file

:white_check_mark: Store user information in a database instead of a text file

:white_check_mark: Use threading to remove inactive sessions

:white_check_mark: Accept code submit requests from the frontend

:white_check_mark: Execute code from the frontend

:white_check_mark: Send code back to the frontend

:white_check_mark: Use threads to run code asynchronously and check if the code runs for too long, then kill the thread and notifiy the user.

:white_check_mark: Do not allow users to create an account with an already existing username.

:white_check_mark: Require emails for registration to prevent users from creating multiple accounts

:white_check_mark: Add email verification

:white_check_mark: Send emails to the users

:white_check_mark: Track users by a unique user id

:white_check_mark: Add multiple questions per page with submission for each question

:white_check_mark: Add email to domain to send emails to users

:white_check_mark: Use DNS records to have verificaiton emails look the least like spam emails to email services:
<ul>
  <li>DKIM</li>
  <li>SPF</li>
  <li>DEMARC</li>
  <li>MX</li>
</ul>

:x: Prevent users from logging into their accounts in multiple windows/tabs/computers

## Functionality of Pages

### Register
<ol>
  <li>User clicks register button on the register page</li>
  <li>Javascript checks if the fields have been entered correctly. The Javascript searches for a "@" in the email field and the password is longer than eight characters. If the conditions are met, the information is sent to the backend</li>
  <li>The backend checks if the user already exits by both email and username.</li>
  <li>The backend saves the information and sends an email to the user. Note that at this time an account is not created. Register information is stored in RAM and will be saved to disk when the user confirms their email</li>
  <li>The sent attribute is set to true to prevent the user recieving multiple emails with the same verification link</li>
  <li>Once the user clicks on the verify link in the email, the register information is used to create a new account along with no completions for the challenges. The register information is then removed from RAM</li>
  <li>The user is automatically logged in on the window they opened the register link in.</li>
</ol>

### Login
<ol>
  <li>User enters login credentials</li>
  <li>Backend hashes the password five times, creates a session token, and an expiration date for the token.</li>
  <li>Token (and only the token) is sent back to the front end to be part of the front-end HTML through a cookie</li>
  <li>The user is sent to the challenges page</li>
</ol>

### Loading a Webpage 
<ol>
  <li>Session token, and any other information is sent to back end</li>
  <li>Backend checks if token is expired. Yes -> require the user to log in. No -> Continue</li>
  <li>Determine the next page that needs to be loaded.</li>
  <li>Send information about the next page to the front end or redirect the user to the correct page</li>
</ol>

### Submitting Code
<ol>
  <li>Encode with base64 the user's code and challengename plus the challenge id and add it to a request along with the user's session token</li>
  <li>Send this data to the backend using ajax</li>
  <li>The backend checks if the recieved session token is valid. Yes -> continue; No -> Require the user to login.</li>
  <li>Decode the base64 encoded user code</li>
  <li>Check if the code contains any statements that allow remote code execution. Examples would be "import" or "write" to write to a file and gain a remote shell to the server</li>
  <li>Run the code</li>
  <li>Save the code to send back to the user if they come back to the page later</li>
  <li>Check if the output matches the expected output Yes -> Mark it as correct; No -> Mark it as correct</li>
  <li>Return the output of the code and whether it was correct or not</li>
  <li>Javascript in the page then checks if all the questions on the page are correct. If they are, then it makes a request to the backend to mark that page complete</li>
</ol>

## Database Layout

### Accounts

The Accounts database contains usernames, emails, hashed passwords, and admin status

Example table:
<table>
  <tr>
    <th>username</th>
    <th>email</th>
    <th>UID</th>
    <th>password</th>
    <th>admin</th>
  </tr>
  <tr>
    <td>Daniel</td>
    <td>daniel@codemonkey.tk</td>
    <td>Gu6jacXMyccsg3TxP3N4tPws6d3ESyR4uBYENqVLja9ZicISgj</td>
    <td>30cd2f99101cdd52cc5fda1e996ee137</td>
    <td>True</td>
  </tr>
  <tr>
    <td>ChrisMz</td>
    <td>chrismz@codemonkey.tk</td>
    <td>psx3P7cAhuLhLuIkUVhuieujSZFyIOK6iSBUY9jUPDv2y2mmnb</td>
    <td>7b3b4de00794a247cf8df8e6fbfe19bf</td>
    <td>False</td>
  </tr>
</table>

### ChallengeCompletions

This table tracks challenge completion for each user. It is a dictionary with keys of uid and values of a dictionary. The inner dictionary for each uid has challIDs for keys and the values are arrays containing the state of completeness of the challenge and previously submitted code.

Example table:

<table>
  <tr>
    <th>UID</th>
    <th>0001</th>
    <th>0002</th>
    <th>0003</th>
  </tr>
    <td>Gu6jacXMyccsg3TxP3N4tPws6d3ESyR4uBYENqVLja9ZicISgj</td>
    <td>True,print("Hello World!")</td>
    <td>False,print(1+1)\nprint(10-4)</td>
    <td>False,print("")</td>
  </tr>
    <td>psx3P7cAhuLhLuIkUVhuieujSZFyIOK6iSBUY9jUPDv2y2mmnb</td>
    <td>False,print("This is a test")</td>
    <td>True,print(1+1)\nprint(10-4)\nprint(2.5*5)\nprint(20/2)</td>
    <td>True,int i = 0\nprint("this is a test of concatenation. We will concatenate " + i + " right there")</td>
  </tr>
</table>

### PageCompletions

This table tracks page completion for each user. It is a dictionary with keys of uid and values of a dictionary. The inner dictionary for each uid has pageIDs for keys and the values are the completeness of pages.

Example table:

<table>
  <tr>
    <th>UID</th>
    <th>firstCode</th>
    <th>arithmeticPractice</th>
    <th>thirdCode</th>
  </tr>
    <td>Gu6jacXMyccsg3TxP3N4tPws6d3ESyR4uBYENqVLja9ZicISgj</td>
    <td>True</td>
    <td>False</td>
    <td>False</td>
  </tr>
    <td>psx3P7cAhuLhLuIkUVhuieujSZFyIOK6iSBUY9jUPDv2y2mmnb</td>
    <td>False</td>
    <td>True</td>
    <td>True</td>
  </tr>
</table>
