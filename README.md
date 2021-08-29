# ProductAvailabilityChecker
An easy to use utility to check availability of a product on multiple E-commerce platforms like Amazon, Reliance Digital etc.

## Instructions to run

#### Update the following variables - 

chromeExePath (Executable Path of Chrome.exe)
example - chromeExePath='C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'

fromID (To be Updated with User's Outlook Email ID)
example - fromID='yourOutlookMailID@outlook.com'

receiversID (list of Receivers Email IDs)
example - receiversID=['ABC@gmail.com']

smtpObj.login('user's Email ID','passwordText') (Command to be updated with userId and password)
example - smtpObj.login('yourOutlookMailID@outlook.com','PasswordText')

#### Run the script
For Windows - Double click on the script - ProductAvailabilityCheck.py to run.

### Dependencies - 

Note - Few of the below libraries might require explicit import as well.
- sys
- os
- bs4
- webbrowser
- requests
- logging
- re
- openpyxl
- smtplib
