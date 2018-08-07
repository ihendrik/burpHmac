# BurpHmac
## How to setup extensions and session handling for HMAC signature
In this tutorial, we are going to see how to add python script to Burp extender and setup the session handling rule to run the extender.
Things that we need:
* Python script from https://github.com/malcomvetter/BurpHmac/blob/master/BurpHmac.py 
* Burpsuite any type (free/community/pro)
* jython-standalone

## Setting up BurpSuite extender
After we have the script, now is the time to upload it to Burpsuite. We are going to upload the script to Burp extender so we can run it when the session handling found the invalid session, run macro then the script.
1.	Open Burpsuite
2.	We are going to use the temporary project (free version) just follow the wizard until there are tabs showing on the window
3.	Find “Extender” tab and click it
4.	Next we are going to click “Add”
5.	Load Burp Extension window will opens up
6.	Choose “Python” as the “Extension type”
7.	Select the python script for the “Extension file”
8.	Then click “next”
9.	If everything goes as planned (finger crossed), we will see “HMAC Header Register” and “Session Handling” as the Output for loading the script
10.	Click close
11.	We will see “HMAC Header Script” as an option for Burp Extensions
12.	Make sure the ”Loaded” and “Extension Loaded” at the bottom are checked.

## Setting up Session Handling
In this section, we will create a rule for session handling with an empty macro. Basically, we are creating a rule which will find invalid session (403 on the header) then run macro (which is empty, so skip) which in turn will run the script on the defined scope at the Target scope. 
1.	Click “Project options” tab
2.	Then click “Session” tab in the Project options tab
3.	Click “Add” to open “Session Handling Rule Editor”
4.	Enter “HMAC Header” as the Rule Description
PS: This should be the same with the getActionName return in the script.
def getActionName(self):
        return "HMAC Header"

5.	Click “Add” on the “Rule Action” then choose “Check session is valid”  to open “Session Handling Action Editor” window
6.	Check “HTTP Headers” and uncheck “URL of redirection target” at the Location(s).
7.	Enter “403” for the “Look for expression” and switch “Match indicates” to “Invalid session”
8.	Scroll down a little and check “if session is invalid, perform….”
9.	Select “Run a macro” then click “Add”
10.	When the “Macro Editor” open up, just click “OK”.
11.	Check “After running the macro, invoke burp extensions action handler”
12.	If we uploaded the script (and the script works), then we will see the script name on the dropdown (ex. HMAC Header)
13.	After that, we click “Scope” tab at the top of the window
14.	Check all “Tool Scope”, so this rule will applied to all Burp functions
15.	Choose “Use Suite Scope”. I tried to use the custom scope but it won’t works
16.	Click OK then we will see the rule in the Session Handling Rules option

## Testing HMAC Script
Add packet which response 403 to the repeater. When we click on GO, the session handling rule will be applied and create HMAC-Signature header which will be sent to the server.
