from burp import IBurpExtender
from burp import ISessionHandlingAction
from burp import IParameter
from java.io import PrintWriter
from datetime import datetime
import hashlib
import base64
import sys
import urllib

class BurpExtender(IBurpExtender, ISessionHandlingAction):
    #
    # implement IBurpExtender
    #
    	
    global key;
    def registerExtenderCallbacks(self, callbacks):
        stdout = PrintWriter(callbacks.getStdout(), True)
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("Body Signature")
        stdout.println("Body Signature register")
        callbacks.registerSessionHandlingAction(self)
        stdout.println("Session handling")
        return	

    def getActionName(self):
        return "Body Signature"

    def performAction(self, currentRequest, macroItems):
        key="1234567890Key"
        stdout = PrintWriter(self._callbacks.getStdout(), True)
        stdout.println("performAction")
        requestInfo = self._helpers.analyzeRequest(currentRequest)

        headers = requestInfo.getHeaders()
        
        #acquire body
        msgBody = currentRequest.getRequest()[requestInfo.getBodyOffset():]
        msg=(''.join(chr(i) for i in msgBody))
        messages = msg.split("&")
        for message in messages:
            if(message.split("=")[0]=="Code"):
                MerchantCode=message.split("=")[1]
            if(message.split("=")[0]=="RefNo"):
                RefNo=message.split("=")[1]

        signature = key+MerchantCode+RefNo
        #stdout.println("signature: " + signature)
		
        signature = bytes(signature).encode('utf-8')
        key=bytes(key).encode('utf-8')
        hashsignature = base64.b64encode(hashlib.sha1(signature).digest())
        #stdout.println(hashsignature)
		
        i=0
        for message in messages:
            if(message.split("=")[0]=="Signature"):
                messages[i]="Signature="+ hashsignature
            i=i+1
        msgBody=('&'.join(messages))
        #stdout.println(msgBody)
        
        # Build new Http Message with the new Hash Header
        HTTPmessage = self._helpers.buildHttpMessage(headers, msgBody)
        #stdout.println(HTTPmessage)

        # Update Request with New Header
        currentRequest.setRequest(HTTPmessage)
        return 
